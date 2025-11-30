#!/bin/bash

# Wrapper script to run black code format checker
# You can pass extra args on the command line
# If last arg passed is a .py file then just check
# that file, otherwise check all .py files in packages

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/in_docker.sh
 
cd ${thisdir}/..

last_arg="${!#}"
if [[ $last_arg =~ \.py$ ]]; then
	echo "INFO: checking ${last_arg}"
	poetry run black $*
else
	while read py_path; do
		echo "INFO: checking ${py_path}"
		poetry run black $* $py_path
	done< <(find packages/ -name \*.py | grep -v "__init__.py")
fi
