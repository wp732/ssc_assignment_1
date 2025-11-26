#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/dockersetsrc.sh

docker build \
	--build-arg UID=$(id -u) \
	--build-arg GID=$(id -g) \
	-t ${CNAME}:${CTAG} .
