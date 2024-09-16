#!/usr/bin/env sh
set -eu

ssh "$1" "libcamera-still --viewfinder-mode 9248:6944:10:P --viewfinder-buffer-count 1 --denoise cdn_off --autofocus-mode manual --lens-position " "$2" " --shutter 200000 -o /tmp/photo.jpg"
rm -f /tmp/photo.jpg
rsync --progress "$1":/tmp/photo.jpg /tmp/
feh /tmp/photo.jpg
