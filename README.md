# Tackem

[![Flake8](https://github.com/GaryTheBrown/Tackem/actions/workflows/Checks.yml/badge.svg)](https://github.com/GaryTheBrown/Tackem/actions/workflows/Checks.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
- An All in one system to manage a library of Movies, TV Shows, Music, Games. (In Progress)
- It is capable of ripping Discs (if optical drives are present) and converting it or an ISO into a
selected format before then placing files in the Library. See [Here](##Ripper) for more info
## RUNNING:

```
pip install -r requirements.txt
python3 tackem.py
```

## access:
```
http://[HOSTNAME/IP]:8081
```

## Ripper *[LINUX ONLY]*
This System allows the user to rip Discs to the library.

It is capable of ripping Audio CDs DVD Videos Blu Ray Videos including 3D and 4k
(this is dependent on what optical drive type is used)

The system uses makemkv for videos and cdda2wav for audio discs.

you need to install additional software for this System to work and will not load until they are all installed.

### Installation

REQUIRED: ```makemkv java JRE CCExtractor libcss2 mplayer eject lsblk hwinfo blkid libdiscid0 cdda2wav```

#### Ubuntu commands
```
sudo add-apt-repository ppa:heyarje/makemkv-beta
sudo apt install hwinfo mplayer ffmpeg makemkv-bin makemkv-oss libdvd-pkg default-jre-headless icedax libdiscid0
sudo dpkg-reconfigure libdvd-pkg
git clone https://github.com/CCExtractor/ccextractor.git
sudo apt install cmake gcc libcurl4-gnutls-dev tesseract-ocr libtesseract-dev libleptonica-dev autoconf
cd ccextractor/linux
./autogen.sh
./configure
make
sudo make install
```

#### makemkv settings.conf
```
app_DefaultSelectionString = "+sel:all"
app_DefaultOutputFileName = "{t:N2}"
app_ccextractor = "/usr/local/bin/ccextractor"
```
