#!/bin/bash

# Script to fetch architecture specific sha256 digest for any Dokcer Hub container

REPO=""
VERSION="latest"
while [ $# -ne 0 ]; do
	case $1 in
		-repo )
			shift
			REPO=$1
			;;
		-version )
			shift
			VERSION=$1
			;;
	esac
	shift
done

if [ -z "${REPO}" ]; then
	echo "ERROR: must specify a docker hub repo via -repo" >&2
	exit 255
fi

ARCH=""
case "`uname -m`" in
	aarch64 )
		ARCH="arm64"
		;;
	x86_64 )
		ARCH="amd64"
		;;
	* )
		echo "ERROR: unsupported architecture ${ARCH}" >&2
		exit 255 
		;;
esac

TOKEN=$(curl -s "https://auth.docker.io/token?service=registry.docker.io&scope=repository:$REPO:pull" | jq -r .token)

curl -s -H "Authorization: Bearer $TOKEN" \
     -H "Accept: application/vnd.docker.distribution.manifest.list.v2+json" \
     "https://registry-1.docker.io/v2/$REPO/manifests/${VERSION}" \
| jq -r --arg ARCH "$ARCH" '.manifests[] | select(.platform.architecture==$ARCH and .platform.os=="linux") | .digest'
