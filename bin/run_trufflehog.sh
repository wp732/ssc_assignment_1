#!/bin/bash

# Wrapper script to run Trufflehog secrets scanner
# using the local installed trufflehog binary.

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/in_docker.sh
 
cd ${thisdir}/..

export TERM=dumb
export PYTHONUNBUFFERED=1
trufflehog git \
	--no-update \
	--log-level=5 \
	--no-verification \
	--no-color \
	--branch HEAD \
	--fail \
	file://.
