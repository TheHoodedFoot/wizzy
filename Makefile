all:
	pio run

upload:
	pio run --target upload

serial:
	picocom -b 115200 /dev/ttyACM0

calibrate: src/calibration/calibration.cpp
	bear -- clang++ $(shell pkg-config --cflags opencv4) $(shell pkg-config --libs opencv4) -o $@ $^

basic: src/calibration/videocapture_basic.cpp
	bear -- clang++ $(shell pkg-config --cflags opencv4) $(shell pkg-config --libs opencv4) -o $@ $^


CPPFLAGS = -Wall -Wextra -Wpedantic -Werror -Wfatal-errors# -Wconversion

wizzcam:	src/wizzcam/wizzcam.o src/wizzcam/event_loop.o
	clang++ $(CPPFLAGS) -o $@ $^ $$(pkg-config --libs libevent_pthreads) $$(pkg-config --libs libcamera)
	sed -e '1s/^/[\n/' -e '$$s/,$$/\n]/' src/wizzcam/*.o.json > compile_commands.json

%.o:	%.cpp
	clang++ $(CPPFLAGS) -c -MJ $@.json -o $@ $$(pkg-config --cflags libcamera) $^

.PHONY: 	clean

clean:
	rm -f src/wizzcam/*.o src/wizzcam/*.o.json wizzcam compile_commands.json
