#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/dockersetsrc.sh

docker run \
	-d \
	--name $CNAME \
	-u $(id -u):$(id -g) \
	${CNAME}:${CTAG}
