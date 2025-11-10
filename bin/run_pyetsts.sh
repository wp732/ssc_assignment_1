#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

cd ${thisdir}/..

poetry run pytest tests/
