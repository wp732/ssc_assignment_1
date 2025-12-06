#!/bin/bash

# Wrapper script to run ruff code format checker
# You can pass extra args on the command line

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/in_docker.sh
 
cd ${thisdir}/..

poetry run ruff check $*
