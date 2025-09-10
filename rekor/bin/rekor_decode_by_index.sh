#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

tmp_dir=/tmp/`uuid`
mkdir -p $tmp_dir

rekor_pub=${tmp_dir}/rekor.pub
curl -s https://rekor.sigstore.dev/api/v1/log/publicKey > $rekor_pub

rekor_entry=${tmp_dir}/rekor_entry.json
${thisdir}/rekor_by_index.sh $* > $rekor_entry

rekor_entry_set=${tmp_dir}/rekor_entry_set.txt
jq -r '.[].verification.signedEntryTimestamp' $rekor_entry > $rekor_entry_set

rekor_entry_set_decoded=${tmp_dir}/rekor_entry_set_decoded.txt
base64 -d $rekor_entry_set > $rekor_entry_set_decoded

rekor_entry_message=${tmp_dir}/rekor_entry_message.txt
jq -cj '.[] | del(.attestation, .verification)' $rekor_entry > $rekor_entry_message

openssl dgst -sha256 -verify $rekor_pub -signature $rekor_entry_set_decoded $rekor_entry_message

rm -r -f $tmp_dir
