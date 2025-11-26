#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/dockersetsrc.sh

xfiltdir=${HOME}/junk/xfilt	# exfiltrate files for debugging
mkdir -p $xfiltdir

docker run \
	-d \
	--name $CNAME \
	-u $(id -u):$(id -g) \
	-p 8000:8000 \
	-v ${thisdir}/../:/home/user/app/:rw \
	-v ${xfiltdir}:/xdir/:rw \
	--entrypoint=/home/user/app/testutils/ep.sh \
	${CNAME}:${CTAG}
