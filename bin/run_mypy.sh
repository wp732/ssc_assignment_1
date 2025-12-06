#!/bin/bash

# Wrapper script to run mypy Python type checker
# You can pass extra args on the command line
# If last arg passed is a .py file then just check
# that file, otherwise check all .py files in packages.
# Note: The reason for the two pass scan (where first
# pass is --install-types) is to ensure a scan won't
# fail due to missing type hints packages. Since there
# is no way to know apriori what imports are included
# in which .py files, we use this approach on a per
# file basis.

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/in_docker.sh
 
cd ${thisdir}/..

ret=0
last_arg="${!#}"
if [[ $last_arg =~ \.py$ ]]; then
	echo "INFO: checking ${last_arg}"
	poetry run mypy --install-types --non-interactive $* > /dev/null 2>&1 || true
	poetry run mypy $*
	ret=$?
else
	while read py_path; do
		echo "INFO: checking ${py_path}"
		poetry run mypy --install-types --non-interactive $* $py_path > /dev/null 2>&1 || true
		poetry run mypy $* $py_path
		rc=$?
		[[ $rc -ne 0 ]] && [[ $ret -eq 0 ]] && ret=$rc
	done< <(find packages/ -name \*.py | grep -v "__init__.py")
fi

exit $ret
