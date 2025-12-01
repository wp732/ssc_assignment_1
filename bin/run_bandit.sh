#!/bin/bash

# Wrapper script to run bandit Python SAST scanner
# You can pass extra args on the command line
# If last arg passed is a .py file then just check
# that file, otherwise check all .py files in packages

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/in_docker.sh
 
cd ${thisdir}/..

ret=0
last_arg="${!#}"
if [[ $last_arg =~ \.py$ ]]; then
	echo "INFO: checking ${last_arg}"
	poetry run bandit $*
	ret=$?
else
	while read py_path; do
		echo "INFO: checking ${py_path}"
		poetry run bandit $* $py_path
		rc=$?
		[[ $rc -ne 0 ]] && [[ $ret -eq 0 ]] && ret=$rc
	done< <(find packages/ -name \*.py | grep -v "__init__.py")
fi

exit $ret
