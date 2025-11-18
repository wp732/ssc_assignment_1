#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

usage() {
	echo ""
	echo "usage: $0 [-verbose] [-file <py file path>]"
	echo ""
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
		-h )
			usage
			;;
		* )
			usage
			;;
    esac
    shift
done

cd ${thisdir}/..

poetry run pytest $show_output tests/
