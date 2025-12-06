#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/dockersetsrc.sh

xtra_args=""
squash_sfx=""
while [ $# -ne 0 ]; do
	case $1 in
		-squash )
			squash_sfx="-small"
			xtra_args="--squash"
			;;
	esac
	shift
done

cd $src_dir

export DOCKER_BUILDKIT=1

docker build \
	--build-arg UID=$(id -u) \
	--build-arg GID=$(id -g) \
	-t ${CNAME}${squash_sfx}:${CTAG} \
	$xtra_args . 2>&1 | cat -
