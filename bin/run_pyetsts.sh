#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

show_output=""
py_file=""
while [ $# -ne 0 ]; do
    case $1 in
        -s )
            show_output="-s"
            ;;
        -f )
			shift
            py_file=$1
            ;;
    esac
    shift
done

cd ${thisdir}/..

set -x
poetry run pytest $show_output tests/${py_file}
