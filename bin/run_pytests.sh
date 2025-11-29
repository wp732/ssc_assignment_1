#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`
proj_dir=${thisdir}/..

usage() {
	echo ""
	echo "usage: $0 [-verbose] [-file <py file path>]"
	echo ""
	echo "       -verbose                # Force stdout/stderr to tty"
	echo "       -file <py file path>    # Path to .py file to act on (default all files)"
	echo ""
}

use_citool=0
show_output=""
py_file=""
while [ $# -ne 0 ]; do
    case $1 in
        -citool )
			use_citool=1
            ;;
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

cd $proj_dir

set -x
if [ $use_citool -eq 1 ]; then
	docker run \
		--rm \
		-t \
		--name=citool \
		-u $(id -u):$(id -g) \
		-v ${proj_dir}:/proj_dir:ro \
		citool:latest \
		poetry run pytest $show_output /proj_dir/tests/${py_file}
else
	poetry run pytest $show_output tests/${py_file}
fi
