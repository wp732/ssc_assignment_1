#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`
proj_dir=${thisdir}/..

pkg_path="$1"

if [ ! -z "${pkg_path}" ]; then
	cd $proj_dir
	poetry run deptry -o /tmp/deptry_report.json packages/wp732-rekor-tools/ > /dev/null 2>&1
	cat /tmp/deptry_report.json | jq -r '[.[].module]|unique|join("\n")'
	rm /tmp/deptry_report.json
fi
