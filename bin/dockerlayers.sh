#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/dockersetsrc.sh

docker inspect ${CNAME}:${CTAG} |jq -r '.[].GraphDriver.Data|to_entries[]|.value'|tr ':' '\n'
