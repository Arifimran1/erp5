#!/bin/sh

PACKAGE_LIST="""\
automake1.9
bison
build-essential
cpio
flex
gcc
libbz2-dev
libgdbm-dev
libglib2.0-dev
libjpeg62-dev
libldap2-dev
libncurses5-dev
libneon27-gnutls-dev
libsasl2-dev
libssl-dev
libsvn-dev
libtool
libxml2-dev
libxslt1-dev
make
patch
rpm
subversion
subversion-tools
xvfb
zip
zlib1g-dev\
"""

apt-get install $PACKAGE_LIST $@
