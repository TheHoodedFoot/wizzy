#!/bin/sh

ssh user@192.168.1.75 rpicam-still --output /tmp/feh.jpg --lens-position $1 --autofocus-mode manual --analoggain $2
rm -f /tmp/feh.jpg
rsync -havP user@192.168.1.75:/tmp/feh.jpg /tmp/feh.jpg
feh /tmp/feh.jpg
ssh user@192.168.1.75 rm /tmp/feh.jpg
