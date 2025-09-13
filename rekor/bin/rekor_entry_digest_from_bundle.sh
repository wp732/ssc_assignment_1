#!/bin/bash

# Take the body returned by rekor to cosign and base64 decode it and then extract 
# the rekor digest which can later be used to lookup uuids of that rekor created for the
# artifact entry in the rekor log by passing the digest to rekor_entry_uuids.sh

bundle_path=${1:--}	# if path of cosign bundle file not passed as an arg then use stdin

jq -r '.rekorBundle.Payload.body' $bundle_path |base64 -d|jq -r '.spec.data.hash.value'
