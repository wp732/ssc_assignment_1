#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/dockersetsrc.sh

xfiltdir=${HOME}/junk/xfilt	# exfiltrate files for debugging
mkdir -p $xfiltdir

docker run \
	-d \
	--name $CNAME \
	-u $(id -u):$(id -g) \
	${CNAME}:${CTAG}
