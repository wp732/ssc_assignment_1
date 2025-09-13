#!/bin/bash

entry_digest=$1
if [ -z "${entry_digest}" ]; then
	read entry_digest
fi

curl -s -X POST https://rekor.sigstore.dev/api/v1/index/retrieve \
	-H 'Content-Type: application/json' \
	-d "{\"hash\": \"${entry_digest}\"}" | jq -r '.[]' | {
while read digest; do
	curl -s https://rekor.sigstore.dev/api/v1/log/entries/${digest} | jq '.[].verification.inclusionProof'
done
}
