#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`
proj_dir=${thisdir}/..

source ${thisdir}/in_docker.sh
cd $proj_dir

while read pkg_path; do
	pushd $pkg_path > /dev/null 2>&1
	echo "INFO: Adding any missing import packages for ${pkg_path}"
	while read missing_import; do
		echo "INFO: Adding missing package ${missing_import}"
		poetry add $missing_import
	done< <(${thisdir}/show_missing_imports.sh $pkg_path)
	popd > /dev/null 2>&1
done< <(find packages/ -mindepth 1 -maxdepth 1 -type d)
