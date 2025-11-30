#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`
proj_dir=${thisdir}/..

source ${thisdir}/in_docker.sh
cd $proj_dir

while read pkg_path; do
	echo "INFO: Adding any missing import packages for ${pkg_path}"
	poetry add -D ./${pkg_path}
done< <(find packages/ -mindepth 1 -maxdepth 1 -type d)
