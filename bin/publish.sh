#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`
proj_dir=${thisdir}/..

export POETRY_PYPI_TOKEN_PYPI=`${thisdir}/keepass_get_value.sh pypitok`

cd ${proj_dir}/packages/wp732-rekor-tools
poetry publish
