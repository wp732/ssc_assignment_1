#!/bin/bash

# Script to verify a container has been locally installed

repo=""
version="latest"
while [ $# -ne 0 ]; do
	case $1 in
		-repo )
			shift
			repo=$1
			;;
		-version )
			shift
			version=$1
			;;
	esac
	shift
done

if [ `docker images | grep -c "^${repo}[ ][ ]*${version}[ ]"` -ne 0 ]; then
	exit 0
else
	exit 255
fi
