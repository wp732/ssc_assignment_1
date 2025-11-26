FROM ubuntu:jammy
ENV DEBIAN_FRONTEND=noninteractive
LABEL stage=citoolbasestage

ARG UID
ARG GID
ARG THOG_VER="3.91.1"
ARG THOG_SIG="bd9baa510dfbd96ead20621957b838bf950f4cb84e4249bd3f2a29f19eb79fb0"
ARG THOG_PKG="trufflehog_${THOG_VER}_linux_arm64.tar.gz"

RUN \
	set -x && \
	cd /root && \
	apt -y update && \
	apt -y install curl && \
	groupadd -g ${GID} user && \
	useradd -m -u ${UID} -g ${GID} user

USER user

RUN \
	curl -LO https://github.com/trufflesecurity/trufflehog/releases/download/v${THOG_VER}/${THOG_PKG} && \
	echo "${THOG_SIG} ${THOG_PKG}" | sha256sum -c - && \
	tar zxvf ${THOG_PKG}

CMD ["/bin/sleep","infinity"]
