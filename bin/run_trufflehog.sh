#!/bin/bash

# Wrapper script to run Trufflehog secrets scanner
# using the local installed trufflehog binary.
# Note we use filesystem here instead of git because
# the intent of this script is to run in a CI workflow
# triggered on a git branch push and thus we are not
# looking to scan the entire git repo and all its history,
# but instead we are only looking to scan the pushed
# commits to see if any new secrets were commited on this push.

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/in_docker.sh
 
cd ${thisdir}/..

export TERM=dumb
export PYTHONUNBUFFERED=1

trufflehog filesystem . \
	--no-update \
	--no-verification \
	--no-color \
	--log-level=5 \
	--fail

