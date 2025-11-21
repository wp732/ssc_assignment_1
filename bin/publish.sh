#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

export POETRY_PYPI_TOKEN_PYPI=`${thisdir}/keepass_get_value.sh pypitok`
poetry publish
