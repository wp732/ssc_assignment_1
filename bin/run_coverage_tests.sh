#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

report_missing=""
service=""
while [ $# -ne 0 ]; do
	case $1 in
		-report_missing )
			report_missing="--cov-report=term-missing"
			;;
		-service )
			shift
			service=$1
			;;
	esac
	shift
done

if [ -z "${service}" ]; then
	echo "ERROR: must supply -service <service name>" >&2
	exit 255
fi

cd ${thisdir}/..

set -x
USE_COVERAGE_CMD=1 poetry run pytest --cov=. $report_missing ${service}/tests/
