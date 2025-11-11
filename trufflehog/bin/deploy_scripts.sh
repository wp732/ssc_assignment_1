#!/bin/bash

# Script to install trufflehog runtime scripts

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

thog_dir=${HOME}/.thog
mkdir -p $thog_dir
chmod 700 $thog_dir
cp ${thisdir}/is_version_installed.sh $thog_dir
cp ${thisdir}/scan_local_repo.sh $thog_dir
cd $thog_dir
chmod 700 *.sh
