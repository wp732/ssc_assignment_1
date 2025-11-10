#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

show_output=""
while [ $# -ne 0 ]; do
    case $1 in
        -s )
            show_output="-s"
            ;;
    esac
    shift
done

cd ${thisdir}/..

poetry run pytest $show_output tests/
