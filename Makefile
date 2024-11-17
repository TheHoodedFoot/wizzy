all:
	pio run

upload:
	pio run --target upload

serial:
	picocom -b 115200 /dev/ttyACM0

calibrate:	src/calibration/calibration.cpp
	$(CXX) $(shell pkg-config --cflags opencv4) $(shell pkg-config --libs opencv4) -o $@ $^
