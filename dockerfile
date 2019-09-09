FROM ubuntu:latest

ARG USER=Tackem
ARG UID=1000
ARG GID=1000

RUN useradd -m ${USER} --uid=${UID} \
 && mkdir -p /home/$USER \
 && chown ${uid}:${gid} -R /home/$USER \
 && apt-get update \
 && apt-get install -y git python3.7 python3-pip \
 && cd /usr/bin \
 && ln -s python3 python \
 && rm -rf /var/lib/apt/lists/*

USER $USER

RUN python3 -m pip install -U pip --user \
 && python3 -m pip install -U configobj cherrypy requests pexpect musicbrainzngs gitpython --user

COPY . /app
WORKDIR /app
ENTRYPOINT python3 tackem.py
