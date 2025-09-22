#!/bin/bash

use_zero_indexing=0
while [ $# -ne 0 ]; do
	case $1 in
		-z )
			use_zero_indexing=1
			;;
		* )
			log_index=$1
			break
			;;
	esac
	shift
done

if [ -z "${log_index}" ]; then
	echo "ERROR: must supply log index" >&2
	exit 255
elif [ $use_zero_indexing -eq 1 ]; then
	log_index=`expr $log_index - 1`
fi

curl -s https://rekor.sigstore.dev/api/v1/log/entries?logIndex=$log_index
