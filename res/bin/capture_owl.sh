#!/usr/bin/env sh
set -eu

# TEMP_DIR=$(mktemp -d -t tmp.XXXXXXXX)
# cleanup () {
#         rm -rf "${TEMP_DIR}"
# }
# trap cleanup EXIT

ssh "$1" "libcamera-still --viewfinder-mode 9248:6944:10:P --viewfinder-buffer-count 1 --denoise cdn_off --autofocus-mode manual --lens-position " "$2" " -o /tmp/owlsight.jpg"
rsync --progress "$1":/tmp/owlsight.jpg /tmp/
feh /tmp/owlsight.jpg
