#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/dockersetsrc.sh

cd $proj_dir

export DOCKER_BUILDKIT=1

docker build \
	--build-arg UID=$(id -u) \
	--build-arg GID=$(id -g) \
	-t ${CNAME}:${CTAG} \
	-f ${src_dir}/Dockerfile \
	.
