#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/dockersetsrc.sh

docker rmi -f $CNAME
${thisdir}/dockerclean.sh
