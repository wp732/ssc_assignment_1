FROM ubuntu:jammy
ENV DEBIAN_FRONTEND=noninteractive
LABEL stage=citoolbasestage

ARG UID
ARG GID
ARG USR="user"
ARG GRP="user"
ARG USRGRP="${USR}:${GRP}"
ARG THOG_VER="3.91.1"
ARG THOG_SIG="bd9baa510dfbd96ead20621957b838bf950f4cb84e4249bd3f2a29f19eb79fb0"
ARG THOG_PKG="trufflehog_${THOG_VER}_linux_arm64.tar.gz"

RUN \
	set -x && \
	cd /root && \
	apt -y update && \
	apt -y install curl && \
	apt -y install python3 && \
	apt -y install python3-pip && \
	groupadd -g ${GID} ${GRP} && \
	useradd -m -u ${UID} -g ${GID} ${USR} 

USER ${USRGRP}
WORKDIR /home/${USR}

COPY --chown=${USRGRP} pyproject.toml .

RUN \
	curl -LO https://github.com/trufflesecurity/trufflehog/releases/download/v${THOG_VER}/${THOG_PKG} && \
	echo "${THOG_SIG} ${THOG_PKG}" | sha256sum -c - && \
	tar zxvf ${THOG_PKG} && \
	rm -f ${THOG_PKG} && \
	curl -sSL https://install.python-poetry.org | python3 - && \
	echo 'export PATH="/home/user/.local/bin:$PATH' >> /home/${USR}/.bashrc && \
	poetry init && \
	poetry install --no-root && \
	poetry add --dev pylint && \
	poetry add --dev black && \
	poetry add --dev ruff && \
	poetry add --dev mypy && \
	poetry add --dev bandit && \
	poetry add --dev doq

CMD ["/bin/sleep","infinity"]
