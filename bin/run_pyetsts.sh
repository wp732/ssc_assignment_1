#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

usage() {
	echo ""
	echo "usage: $0 -service <service name> [-verbose] [-file <py file path>]"
	echo ""
	echo "       -service <service name> # Specify service directory name within this project"
	echo "                               # For example rekor to act on rekor/src"
	echo "       -verbose                # Force stdout/stderr to tty"
	echo "       -file <py file path>    # Path to .py file to act on (default all files)"
	echo ""
}

show_output=""
py_file=""
service=""
while [ $# -ne 0 ]; do
    case $1 in
        -verbose )
            show_output="-s"
            ;;
        -file )
			shift
            py_file=$1
            ;;
        -service )
            shift
            service=$1
            ;;
		-h )
			usage
			;;
		* )
			usage
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
poetry run pytest $show_output ${service}/tests/${py_file}
