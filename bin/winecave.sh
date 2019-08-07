#!/bin/sh
#
# created: 2018.10.23
# author : k.inokuchi
#

/usr/sbin/i2cdetect -y 1 > /dev/null
/usr/bin/python3 /opt/winecave/bin/winecave.py
