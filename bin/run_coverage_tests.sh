#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

report_missing=""
while [ $# -ne 0 ]; do
	case $1 in
		-report_missing )
			report_missing="--cov-report=term-missing"
			;;
	esac
	shift
done

source ${thisdir}/in_docker.sh

cd ${thisdir}/..

USE_COVERAGE_CMD=1 poetry run pytest --cov=. $report_missing tests/
