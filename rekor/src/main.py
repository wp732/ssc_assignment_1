import argparse
from util import get_nested_field_by_name, base64_decode, base64_decode_as_dict, extract_public_key, verify_artifact_signature
from merkle_proof import DefaultHasher, verify_consistency, verify_inclusion, compute_leaf_hash
import json
import requests
import sys
from pathlib import Path
import os

def write_checkpoint_file(checkpoint):
	chkpnt_file = str(Path.home())+"/checkpoint.json"
	fd = os.open(chkpnt_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
	with os.fdopen(fd, 'w') as f:
		f.write(json.dumps(checkpoint))

def get_log_entry(log_index, debug=False):
	entry=None
	response = requests.get(f"https://rekor.sigstore.dev/api/v1/log/entries?logIndex={log_index}")
	if response is not None and response.status_code == 200:
		entry=response.json()
		if debug:
			print(json.dumps(entry, indent=4))
	else:
		print("ERROR: get_latest_checkpoint had invalid response", file=sys.stderr)
	return entry

def get_verification_proof(log_index, debug=False):
	inclusion_proof=None
	entry = get_log_entry(log_index, debug)
	if entry is not None:
		verification = get_nested_field_by_name(entry, "verification")
		inclusion_proof = verification['inclusionProof']
	return inclusion_proof

# WP
def get_log_consistency_proof(tree_id, current_tree_size, previous_tree_size):
	consistency_proof=None
	response = requests.get(f"https://rekor.sigstore.dev/api/v1/log/proof?firstSize={previous_tree_size}&lastSize={current_tree_size}&treeId={tree_id}")
	if response is not None and response.status_code == 200:
		consistency_proof=response.json()
	else:
		print("ERROR: get_log_consistency_proof had invalid response", file=sys.stderr)
	return consistency_proof

# WP
def get_log_entry_body_encoded(entry):
	return get_nested_field_by_name(entry, "body")

# WP
def get_log_entry_body_decoded(entry):
	return base64_decode_as_dict(get_log_entry_body_encoded(entry))

# WP
def get_base64_log_entry_artifact_signature_from_body(body):
	if body['kind'] == "hashedrekord":
		return body['spec']['signature']['content']

# WP
def get_base64_log_entry_artifact_signing_cert_from_body(body):
	if body['kind'] == "hashedrekord":
		return body['spec']['signature']['publicKey']['content']

def inclusion(log_index, artifact_filepath, debug=False):
	# Get entry from Rekor log by logIndex
	entry = get_log_entry(log_index)

	# Get decoded body from Rekor log entry
	body = get_log_entry_body_decoded(entry)

	# Get decoded artifact signature from body data
	signature = base64_decode(get_base64_log_entry_artifact_signature_from_body(body))

	# Get decoded certificate from body data
	certificate = base64_decode(get_base64_log_entry_artifact_signing_cert_from_body(body))

	# Get public key (in PEM format) from certificate
	public_key = extract_public_key(certificate)

	# Use the DSA algorithm to verify the artifact signature
	verify_artifact_signature(signature, public_key, artifact_filepath)

	# Get inclusionProof from the Rekor log entry
	inclusion_proof = get_verification_proof(log_index)
	if inclusion_proof is not None:
		# Note: Rekor log is implemented as a Merkle Tree (MT)
		root_hash = inclusion_proof['rootHash'] # rootHash of MT at time entry was added
		tree_size = inclusion_proof['treeSize'] # treeSize of MT at time entry was added
		leaf_hash = compute_leaf_hash(get_log_entry_body_encoded(entry)) # sha256 of null prefixed body
		hashes = inclusion_proof['hashes'] # MT sibling node hashes
		index = inclusion_proof['logIndex'] # monotonic sequence number assinged when entry was included
		
		# Verification is by way of deriving a rootHash from inclusionProof sibling hashes and leaf hash
		# and comparing that to rootHash from inclusionProof
		verify_inclusion(DefaultHasher, index, tree_size, leaf_hash, hashes, root_hash)
		print("Offline root hash calculation for inclusion verified")

def get_latest_checkpoint(debug=False):
	checkpoint=None
	response = requests.get('https://rekor.sigstore.dev/api/v1/log')
	if response is not None and response.status_code == 200:
		checkpoint=response.json()
		if debug:
			write_checkpoint_file(checkpoint)
	else:
		print("ERROR: get_latest_checkpoint had invalid response", file=sys.stderr)
	return checkpoint

def consistency(prev_checkpoint, debug=False):
	checkpoint = get_latest_checkpoint(debug)
	if checkpoint is not None \
	and prev_checkpoint is not None \
	and prev_checkpoint["treeID"] == checkpoint["treeID"]:
		consistency_proof=get_log_consistency_proof(checkpoint["treeID"], checkpoint["treeSize"], prev_checkpoint["treeSize"])
		if consistency_proof is not None:
			verify_consistency(
				DefaultHasher,
				prev_checkpoint["treeSize"],
				checkpoint["treeSize"],
				consistency_proof["hashes"],
				prev_checkpoint["rootHash"],
				checkpoint["rootHash"]
			)
			print("Consistency verification successful.")

def main():
	debug = False
	parser = argparse.ArgumentParser(description="Rekor Verifier")
	parser.add_argument('-d', '--debug', help='Debug mode',
						required=False, action='store_true') # Default false
	parser.add_argument('-c', '--checkpoint', help='Obtain latest checkpoint\
						from Rekor Server public instance',
						required=False, action='store_true')
	parser.add_argument('--inclusion', help='Verify inclusion of an\
						entry in the Rekor Transparency Log using log index\
						and artifact filename.\
						Usage: --inclusion 126574567',
						required=False, type=int)
	parser.add_argument('--artifact', help='Artifact filepath for verifying\
						signature',
						required=False)
	parser.add_argument('--consistency', help='Verify consistency of a given\
						checkpoint with the latest checkpoint.',
						action='store_true')
	parser.add_argument('--tree-id', help='Tree ID for consistency proof',
						required=False)
	parser.add_argument('--tree-size', help='Tree size for consistency proof',
						required=False, type=int)
	parser.add_argument('--root-hash', help='Root hash for consistency proof',
						required=False)
	parser.add_argument('-e', '--entry', help='Get Rekor log entry by log index\
						Usage: --entry 126574567',
						required=False, type=int)
	args = parser.parse_args()
	if args.debug:
		debug = True
		print("enabled debug mode")
	if args.checkpoint:
		# get and print latest checkpoint from server
		# if debug is enabled, store it in a file checkpoint.json
		checkpoint = get_latest_checkpoint(debug)
		if checkpoint is not None:
			print(json.dumps(checkpoint, indent=4))
	if args.inclusion:
		inclusion(args.inclusion, args.artifact, debug)
	if args.entry:
		get_log_entry(args.entry, debug)
	if args.consistency:
		if not args.tree_id:
			print("please specify tree id for prev checkpoint")
			return
		if not args.tree_size:
			print("please specify tree size for prev checkpoint")
			return
		if not args.root_hash:
			print("please specify root hash for prev checkpoint")
			return

		prev_checkpoint = {}
		prev_checkpoint["treeID"] = args.tree_id
		prev_checkpoint["treeSize"] = args.tree_size
		prev_checkpoint["rootHash"] = args.root_hash

		consistency(prev_checkpoint, debug)

if __name__ == "__main__":
	main()
