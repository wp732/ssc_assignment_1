#!/bin/bash

# Script to build the pacakge. Since the output whl should
# include an SBOM that reflects the state of the package configuration
# at build time this script will call the script to generate an SBOM
# each time it is run.

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`
proj_dir=${thisdir}/..

echo "INFO: removing old dist/ dir"
rm -r -f ${proj_dir}/packages/wp732-rekor-tools/dist/

${proj_dir}/bin/sbom_create.sh
[[ $? -ne 0 ]] && exit 255

cd ${proj_dir}/packages/wp732-rekor-tools
echo "INFO: Building package"
poetry build
