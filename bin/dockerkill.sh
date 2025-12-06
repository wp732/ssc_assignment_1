#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/dockersetsrc.sh

docker kill $CNAME
if [ "$1" == "-rm" ]; then
	docker rm $CNAME
fi
