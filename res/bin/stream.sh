#!/bin/sh

ssh user@192.168.1.75 rpicam-vid -t 0 --inline --listen -o tcp://0.0.0.0:9999 --width=1920 --height=1080 &
sleep 1
ffplay tcp://192.168.1.75:9999 -vf "setpts=N/30" -fflags nobuffer -flags low_delay -framedrop
