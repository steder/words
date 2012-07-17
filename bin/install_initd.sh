#!/usr/bin/env bash
set -e -u -x

cp etc/words_initd.sh /etc/init.d/words
chmod +x /etc/init.d/words