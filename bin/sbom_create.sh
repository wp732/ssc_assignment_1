#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`
proj_dir=${thisdir}/..

pkg_name="wp732-rekor-tools"
pkg_dir=${proj_dir}/packages/${pkg_name}

dist_dir=${pkg_dir}/dist
mkdir -p $dist_dir

# Create a temporary symlink to poetry.lock
# (cyclonedx-py won't work for monorepo poetry packaging without this).

cd $pkg_dir
ln -s ${proj_dir}/poetry.lock poetry.lock

cd $proj_dir
echo "INFO: Creating SBOM (this will take awhile)..."
poetry run cyclonedx-py poetry \
	--no-dev \
	-o ${dist_dir}/cyclonedx-sbom.json \
	 packages/${pkg_name}

cd $pkg_dir
rm poetry.lock 
