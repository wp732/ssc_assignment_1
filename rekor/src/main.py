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
	# verify that log index value is sane
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
	# verify that log index value is sane
	pass

def get_log_entry_body_decoded(entry):
	return base64_decode_as_dict(get_nested_field_by_name(entry, "body"))

def get_base64_log_entry_artifact_signature_from_body(body):
	if body['kind'] == "hashedrekord":
		return body['spec']['signature']['content']

def get_base64_log_entry_artifact_signing_cert_from_body(body):
	if body['kind'] == "hashedrekord":
		return body['spec']['signature']['publicKey']['content']

def inclusion(log_index, artifact_filepath, debug=False):
	entry = get_log_entry(log_index)
	body = get_log_entry_body_decoded(entry)
	signature = get_base64_log_entry_artifact_signature_from_body(body)
	# verify that log index and artifact filepath values are sane

	certificate = base64_decode(get_base64_log_entry_artifact_signing_cert_from_body(body))
	public_key = extract_public_key(certificate)
	verify_artifact_signature(signature, public_key, artifact_filepath)
	# get_verification_proof(log_index)
	# verify_inclusion(DefaultHasher, index, tree_size, leaf_hash, hashes, root_hash)

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
	# verify that prev checkpoint is not empty
	# get_latest_checkpoint()
	pass

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
