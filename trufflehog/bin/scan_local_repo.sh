#!/bin/bash

which dockerx > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: docker not installed! Install docker and run trufflehog/bin/install.sh first."
    exit 255
fi

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

GIT_PROJECT_ROOT_DIR=${GIT_PROJECT_ROOT_DIR:-$(pwd)}

repo="trufflesecurity/trufflehog"
version="latest"

if [ ! -d $GIT_PROJECT_ROOT_DIR ]; then
	echo "ERROR: cannot read dir ${GIT_PROJECT_ROOT_DIR}" >&2
	exit 255
fi

${thisdir}/is_version_installed.sh -repo $repo -version $version
if [ $? -eq 0 ]; then
	echo ""
	echo "`date -u` INFO: Starting Trufflehog scan. This will take awhile..."
	echo ""
	docker run \
		--rm \
		-t \
		-e TERM=dumb \
		-e PYTHONUNBUFFERED=1 \
		-v "${GIT_PROJECT_ROOT_DIR}:/repo:ro" \
		${repo}:${version} \
		git \
		--no-update \
		--log-level=5 \
		--no-verification \
		--no-color \
		--branch HEAD \
		--fail \
		file:///repo
	rc=$?
	echo ""
	if [ $rc -ne 0 ]; then
		echo "`date -u` ERROR: secret found"
	else
		echo "`date -u` INFO: no secrets found"
	fi
	exit $rc
else
	echo ""
	echo "ERROR: ${repo}:${version} not locally installed" >&2
	exit 255
fi
