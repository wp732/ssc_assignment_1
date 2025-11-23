#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

pass_args=""
use_verify=0
use_print_msg=0
use_print_body=0
while [ $# -ne 0 ]; do
	case $1 in
		-v )	# verify log entry signature
			use_verify=1
			;;
		-m )	# print log entry
			use_print_msg=1
			;;
		-b )	# print log entry body
			use_print_body=1
			;;
		* )
			pass_args="${pass_args} $1"
			;;
	esac
	shift
done

tmp_dir=/tmp/`uuid`
mkdir -p $tmp_dir

rekor_pub=${tmp_dir}/rekor.pub
curl -s https://rekor.sigstore.dev/api/v1/log/publicKey > $rekor_pub

rekor_entry=${tmp_dir}/rekor_entry.json
${thisdir}/rekor_entry_by_log_index.sh $pass_args > $rekor_entry

rekor_entry_set=${tmp_dir}/rekor_entry_set.txt
jq -r '.[].verification.signedEntryTimestamp' $rekor_entry > $rekor_entry_set

rekor_entry_set_decoded=${tmp_dir}/rekor_entry_set_decoded.txt
base64 -d $rekor_entry_set > $rekor_entry_set_decoded

rekor_entry_message=${tmp_dir}/rekor_entry_message.txt
jq -cj '.[] | del(.attestation, .verification)' $rekor_entry > $rekor_entry_message

if [ $use_verify -eq 1 ]; then
	openssl dgst -sha256 -verify $rekor_pub -signature $rekor_entry_set_decoded $rekor_entry_message
fi

if [ $use_print_msg -eq 1 ]; then
	cat $rekor_entry_message
fi

if [ $use_print_body -eq 1 ]; then
	jq -r '.body' $rekor_entry_message | base64 -d
fi

rm -r -f $tmp_dir
