FROM ubuntu:latest

ENV TZ=Europe/London
ARG USER=Tackem
ARG UID=1000
ARG GID=1000

COPY . /app
WORKDIR /app

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
 && useradd -m ${USER} --uid=${UID} \
 && mkdir -p /home/${USER}/.MakeMKV \
 && chown ${uid}:${gid} -R /home/$USER \
 && apt-get update \
 && apt-get install -y software-properties-common \
 && add-apt-repository -y ppa:heyarje/makemkv-beta \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y git python3.9 python3-pip makemkv-bin hwinfo eject mplayer ffmpeg default-jre-headless icedax libdiscid0 ccextractor libdvd-pkg \
 && dpkg-reconfigure libdvd-pkg --frontend=noninteractive \
 && ln -s python3 python \
 && echo 'app_DefaultSelectionString = "+sel:all"' > /home/${USER}/.MakeMKV/settings.conf \
 && echo 'app_DefaultOutputFileName = "{t:N2}"' >> /home/${USER}/.MakeMKV/settings.conf \
 && echo 'app_ccextractor = "/usr/bin/ccextractor"' >> /home/${USER}/.MakeMKV/settings.conf \
 && python3 -m pip install pip \
 && python3 -m pip install -r /app/requirements.txt

USER $USER

ENTRYPOINT python3 tackem.py
