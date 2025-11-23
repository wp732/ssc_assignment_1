#!/bin/bash

# Script to sign and attest the package whl combined with package SBOM

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`
proj_dir=${thisdir}/..

pkg_name="wp732-rekor-tools"
pkg_dir=${proj_dir}/packages/${pkg_name}

dist_dir=${pkg_dir}/dist

pkg_ver=`${thisdir}/get_package_version.sh`

cd $proj_dir

read -n1 -s -r -p "Sign into GitHub first, then press any key to continue..."
echo ""

set -x
cosign attest-blob \
	--bundle ${dist_dir}/sbom-attestation.bundle \
	--output-attestation ${HOME}/${pkg_name}_attest.json \
	--predicate ${dist_dir}/cyclonedx-sbom.json \
	--type cyclonedx \
	${dist_dir}/wp732_rekor_tools-${pkg_ver}-py3-none-any.whl > ${HOME}/whl_attest.out
