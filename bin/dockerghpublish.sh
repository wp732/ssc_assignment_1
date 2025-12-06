#!/bin/bash

thisdir=`(cd \`dirname $0\` > /dev/null 2>&1; pwd)`

source ${thisdir}/dockersetsrc.sh

${thisdir}/keepass_get_value.sh ghcr_admin | docker login ghcr.io -u wp732 --password-stdin

local_image="${CNAME}:${CTAG}"
remote_image=ghcr.io/wp732/${local_image}

docker tag $local_image $remote_image
docker push $remote_image
