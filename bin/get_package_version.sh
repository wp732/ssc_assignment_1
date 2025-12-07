#!/bin/bash

# Script to get package verion from latest git tag

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`
proj_dir=${thisdir}/..
git describe --tags --abbrev=0 | sed 's/^v//'
