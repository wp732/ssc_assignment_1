#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/dockersetsrc.sh

cd $src_dir

	#-f ${src_dir}/Dockerfile \
export DOCKER_BUILDKIT=1

docker build \
	--build-arg UID=$(id -u) \
	--build-arg GID=$(id -g) \
	-t ${CNAME}:${CTAG} \
	. 2>&1 | cat -
