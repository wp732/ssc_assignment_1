#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

cd ${thisdir}/..

find . -name "*.egg-info" -type d -exec rm -rf {} +
find . -name "__pycache__" -type d -exec rm -rf {} +
