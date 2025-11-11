#!/bin/bash

# Script to install trufflehog container from Docker Hub

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

repo="trufflesecurity/trufflehog"

version="latest"
while [ $# -ne 0 ]; do
	case $1 in
		-version )
			shift
			version=$1
			;;
	esac
	shift
done

digest=`${thisdir}/get_digest.sh -repo ${repo} -version ${version}`
[[ $? -ne 0 ]] && exit 255

docker pull ${repo}@${digest}
[[ $? -ne 0 ]] && exit 255

image_id=`docker images | grep "^${repo}[ ][ ]*[<]none[>]" | awk '{print $3}'`
if [ ! -z "${image_id}" ]; then
	docker tag $image_id ${repo}:${version}
fi
