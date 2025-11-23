#!/bin/bash

# Script to get package verion from pyproject.toml

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`
proj_dir=${thisdir}/..
cat ${proj_dir}/packages/wp732-rekor-tools/pyproject.toml | tr '\t' ' ' | grep "^[ ]*version[ ]*[=]" | tr -d '"' | awk '{print $NF}'
