FROM ubuntu:noble
ENV DEBIAN_FRONTEND=noninteractive
LABEL stage=citoolbasestage

ARG UID
ARG GID
ARG USR="ubuntu"
ARG GRP="ubuntu"
ARG USRGRP="${USR}:${GRP}"
ARG THOG_VER="3.91.1"
ARG THOG_SIG="bd9baa510dfbd96ead20621957b838bf950f4cb84e4249bd3f2a29f19eb79fb0"
ARG THOG_PKG="trufflehog_${THOG_VER}_linux_arm64.tar.gz"
ARG POETRY_BIN_DIR="/home/${USR}/.local/share/pypoetry/venv/bin"

SHELL ["/bin/bash", "-c"]

RUN \
	set -x && \
	cd /root && \
	getent passwd ${UID} && \
	if [ $? -ne 0 ]; then \
		groupadd -g ${GID} ${GRP}; \
		useradd -m -u ${UID} -g ${GID} ${USR}; \
	fi && \
	apt -y update && \
	apt -y install curl && \
	apt -y install python3 && \
	apt -y install python3-pip

LABEL stage=citoolrootstage

USER ${USRGRP}
WORKDIR /home/${USR}

RUN \
	mkdir -p /home/${USR}/.local/bin && \
	echo "export PATH=\"/home/${USR}/.local/bin:${PATH}\"" >> /home/${USR}/.bashrc && \
	curl -LO https://github.com/trufflesecurity/trufflehog/releases/download/v${THOG_VER}/${THOG_PKG} && \
	echo "${THOG_SIG} ${THOG_PKG}" | sha256sum -c - && \
	tar zxvf ${THOG_PKG} && \
	rm -f ${THOG_PKG} && \
	mv /home/${USR}/trufflehog /home/${USR}/.local/bin/

LABEL stage=citooltfhogstage

RUN \
	curl -sSL https://install.python-poetry.org | python3 - && \
	export PATH="${PATH}:${POETRY_BIN_DIR}" && \
	poetry init --no-interaction

LABEL stage=citoolpoetry1stage

ENV HOME="/home/${USR}"
ENV PATH="${HOME}/.local/bin:${PATH}"
COPY --chown=${USRGRP} pyproject.toml .

RUN \
	poetry install --no-root

LABEL stage=citoolpoetry2stage

RUN \
	echo '#!/bin/sh' > ${HOME}/docker-entrypoint.sh && \
	echo 'set -x' >> ${HOME}/docker-entrypoint.sh && \
	echo 'echo "args: $*"' >> ${HOME}/docker-entrypoint.sh && \
	echo "exec \"${HOME}/.local/bin/\$@\"" >> ${HOME}/docker-entrypoint.sh && \
	chmod 555 ${HOME}/docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD []
