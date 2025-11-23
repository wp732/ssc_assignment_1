"""Program for handling Rekor log entry verifications."""

import os
import stat
import sys
import json
from pathlib import Path
import argparse
import requests
from wp732.rekor_tools.util import (
    get_nested_field_by_name,
    base64_decode,
    base64_decode_as_dict,
    extract_public_key,
    verify_artifact_signature,
)
from wp732.rekor_tools.merkle_proof import (
    DefaultHasher,
    verify_consistency,
    verify_inclusion,
    compute_leaf_hash,
)

USER_RW_ACCESS = stat.S_IRUSR | stat.S_IWUSR


def write_checkpoint_file(checkpoint):
    """Function to persist a Rekor checkpoint file to home directory.

    Args:
        checkpoint: checkpoint object returned from API call to Rekor.

    Returns:
        None:

    Raises:
        Exception or Error: Various exceptions from syscalls are possible.
    """
    chkpnt_file = str(Path.home()) + "/checkpoint.json"
    fd = os.open(
        chkpnt_file,
        os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
        USER_RW_ACCESS
    )
    with os.fdopen(fd, "w") as f:
        f.write(json.dumps(checkpoint))


def get_log_entry(log_index, debug=False):
    """Get a Rekor log entry object via Rekor API call.

    Args:
        log_index: The logIndex for the Rekor log entry.
        debug: Enable or disable debugging.

    Returns:
        dict or None: A Rekor log entry object or None if log entry not found.

    """
    entry = None
    response = requests.get(
        f"https://rekor.sigstore.dev/api/v1/log/entries?logIndex={log_index}",
        timeout=10
    )
    if response.status_code == 200:
        entry = response.json()
        if debug:
            print(json.dumps(entry, indent=4))
    else:
        print(
            f"ERROR: get_latest_checkpoint"
            f" had invalid response code = {response.status_code}",
            file=sys.stderr
        )
    return entry


def get_verification_proof(log_index, debug=False):
    """Get inclusionProof from specific Rekor log entry.

    Args:
        log_index: logIndex of Rekor log entry to search for.
        debug: Enable or disable debugging.

    Returns:
        dict or None: The inclusionProof is returned if one exists.

    """
    inclusion_proof = None
    entry = get_log_entry(log_index, debug)
    if entry is not None:
        verification = get_nested_field_by_name(entry, "verification")
        inclusion_proof = verification["inclusionProof"]
    return inclusion_proof


# WP
def get_log_consistency_proof(tree_id, current_tree_size, previous_tree_size):
    """Get Consistency proof

    Args:
        tree_id:
        current_tree_size:
        previous_tree_size:

    Returns:
        dict or None: On success a dict of all hashes required to compute a
            consistency proof is returned.
    """
    consistency_proof = None
    response = requests.get(
        f"https://rekor.sigstore.dev/api/v1/log/proof"
        f"?firstSize={previous_tree_size}"
        f"&lastSize={current_tree_size}"
        f"&treeId={tree_id}",
        timeout=10
    )
    if response.status_code == 200:
        consistency_proof = response.json()
    else:
        print(
            f"ERROR: get_log_consistency_proof"
            f" had invalid response code = {response.status_code}",
            file=sys.stderr
        )
    return consistency_proof


# WP
def get_log_entry_body_encoded(entry):
    """Get log entry body from a Rekor log entry object.

    Args:
        entry: A Rekor log entry object.

    Returns:
        base64 str or None: On success the base64 encoded body from a
            Rekor log entry object is returned.
    """
    return get_nested_field_by_name(entry, "body")


# WP
def get_log_entry_body_decoded(entry):
    """Get base64 decoded log entry body from a Rekor log entry object.

    Args:
        entry: A Rekor log entry object.

    Returns:
        dict or None: On success the base64 decoded body from a
            Rekor log entry object is returned.
    """
    return base64_decode_as_dict(get_log_entry_body_encoded(entry))


# WP
def get_base64_log_entry_artifact_signature_from_body(body):
    """Get base64 log entry artifact signature from a Rekor log entry body.

    Args:
        body: A base64 decoded body from a Rekor log entry object.

    Returns:
        str or None: If body of correct kind was passed then
            an artifact signature is returned.
    """
    res = None
    if body["kind"] == "hashedrekord":
        res = body["spec"]["signature"]["content"]
    return res


# WP
def get_base64_log_entry_artifact_signing_cert_from_body(body):
    """Get base64 log entry artifact signing cert from a
        Rekor log entry body object.

    Args:
        body: A base64 decoded body from a Rekor log entry object.

    Returns:
        str or None: If body of correct kind was passed then
            an artifact signing cert is returned.
    """
    res = None
    if body["kind"] == "hashedrekord":
        res = body["spec"]["signature"]["publicKey"]["content"]
    return res


def inclusion(log_index, artifact_filepath, debug=False):
    """Test that a specific log entry exists in Rekor log for a
        given artifact file. Print a confirmation message to stdout on success.

    Args:
        log_index: The logIndex for the Rekor log entry.
        artifact_filepath: The file path of the artifact file that was
            cosgin submitted to Rekor.
        debug: Enable or disable debugging.

    Raises:
        FileNotFoundError: If invalid artifact_filepath specified.
        AttributeError: This can occur if wrong log_index was specified.
    """
    # Get entry from Rekor log by logIndex
    entry = get_log_entry(log_index, debug)

    # Get decoded body from Rekor log entry
    body = get_log_entry_body_decoded(entry)

    # Get decoded artifact signature from body data
    signature = base64_decode(
        get_base64_log_entry_artifact_signature_from_body(body)
    )

    # Get decoded certificate from body data
    certificate = base64_decode(
        get_base64_log_entry_artifact_signing_cert_from_body(body)
    )

    # Get public key (in PEM format) from certificate
    public_key = extract_public_key(certificate)

    # Use the DSA algorithm to verify the artifact signature
    verify_artifact_signature(signature, public_key, artifact_filepath)

    # Get inclusionProof from the Rekor log entry
    inclusion_proof = get_verification_proof(log_index)
    if inclusion_proof is not None:
        # Note: Rekor log is implemented as a Merkle Tree (MT)
        root_hash = inclusion_proof[
            "rootHash"
        ]  # rootHash of MT at time entry was added
        tree_size = inclusion_proof[
            "treeSize"
        ]  # treeSize of MT at time entry was added
        leaf_hash = compute_leaf_hash(
            get_log_entry_body_encoded(entry)
        )  # sha256 of null prefixed body
        hashes = inclusion_proof["hashes"]  # MT sibling node hashes
        index = inclusion_proof[
            "logIndex"
        ]  # monotonic sequence number assinged when entry was included

        # Verification is by way of deriving a rootHash from
        # inclusionProof sibling hashes and leaf hash and
        # comparing that to rootHash from inclusionProof.
        verify_inclusion(
            DefaultHasher, index, tree_size, leaf_hash, hashes, root_hash
        )
        print("Offline root hash calculation for inclusion verified")


def get_latest_checkpoint(debug=False):
    """Get latest checkpoint object from Rekor.
       If debug is enabled then also perist the checkpoint.

    Args:
        debug: Enable or disable debugging.

    Returns:
        dict or None: On success the latest Rekor checkpoint object
            is returned.
    """
    checkpoint = None
    response = requests.get(
        "https://rekor.sigstore.dev/api/v1/log",
        timeout=10
    )
    if response.status_code == 200:
        checkpoint = response.json()
        if debug:
            write_checkpoint_file(checkpoint)
    else:
        print(
            f"ERROR: get_latest_checkpoint"
            f" had invalid response code = {response.status_code}",
            file=sys.stderr
        )
    return checkpoint


def consistency(prev_checkpoint, debug=False):
    """Test the consistency between the current Rekor checkpoint and
        a previously captured checkpoint.
        Print a confirmation message to stdout on success.
       A ERROR message will print of Rekor API response code not 200.

    Args:
        prev_checkpoint:
        debug: Enable or disable debugging.

    Raises:
        ValueError: Can occur if invalid root-hash was speicifed.
        RootMismatchError: If wrong tree-size was specified.
    """
    # Get latest checkpoint from Rekor
    checkpoint = get_latest_checkpoint(debug)
    if (
        checkpoint is not None
        and prev_checkpoint is not None
    ):
        if prev_checkpoint["treeID"] == checkpoint["treeID"]:
            # Get consistency proof object from Rekor
            consistency_proof = get_log_consistency_proof(
                checkpoint["treeID"],
                checkpoint["treeSize"],
                prev_checkpoint["treeSize"],
            )
            if consistency_proof is not None:
                verify_consistency(
                    DefaultHasher,
                    prev_checkpoint["treeSize"],
                    checkpoint["treeSize"],
                    consistency_proof["hashes"],
                    prev_checkpoint["rootHash"],
                    checkpoint["rootHash"],
                )
                print("Consistency verification successful.")
            else:
                print(
                    f"ERROR: consistencyProof not found for "
                    f" checkpoint with rootHash={checkpoint['rootHash']}"
                    f" in Rekor tree={checkpoint['treeID']}",
                    file=sys.stderr
                )
        else:
            print(
                f"ERROR: Consistency check failed due to treeId mismatch."
                f" Previous checkpoint treeId={prev_checkpoint['treeID']}"
                f" Current checkpoint treeId={checkpoint['treeID']}",
                file=sys.stderr
            )


def main():
    """main.
    """
    debug = False
    parser = argparse.ArgumentParser(description="Rekor Verifier")
    parser.add_argument(
        "-d", "--debug", help="Debug mode", required=False, action="store_true"
    )  # Default false
    parser.add_argument(
        "-c",
        "--checkpoint",
        help="Obtain latest checkpoint\
            from Rekor Server public instance. When used with -d also saves \
            the checkpoint to ~/checkpoint.json",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--inclusion",
        help="Verify inclusion of an\
            entry in the Rekor Transparency Log using log index\
            and artifact filename.\
            Usage: --inclusion 126574567",
        required=False,
        type=int,
    )
    parser.add_argument(
        "--artifact",
        help="Artifact filepath for verifying\
            signature",
        required=False,
    )
    parser.add_argument(
        "--consistency",
        help="Verify consistency of a given\
            checkpoint with the latest checkpoint.",
        action="store_true",
    )
    parser.add_argument(
        "--tree-id", help="Tree ID for consistency proof", required=False
    )
    parser.add_argument(
        "--tree-size",
        help="Tree size for consistency proof",
        required=False,
        type=int,
    )
    parser.add_argument(
        "--root-hash", help="Root hash for consistency proof", required=False
    )
    parser.add_argument(
        "-e",
        "--entry",
        help="Get Rekor log entry by log index\
            Usage: --entry 126574567",
        required=False,
        type=int,
    )
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
        log_entry_dict = get_log_entry(args.entry, debug)
        if log_entry_dict is not None:
            print(json.dumps(log_entry_dict), flush=True)
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
