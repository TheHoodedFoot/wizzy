all:
	pio run

upload:
	pio run --target upload

serial:
	picocom -b 115200 /dev/ttyACM0

calibrate2:	src/calibration/calibration.cpp
	$(CXX) $(shell pkg-config --cflags opencv4) -o $@ $^ -lopencv_stitching -lopencv_alphamat -lopencv_aruco -lopencv_bgsegm -lopencv_bioinspired -lopencv_ccalib -lopencv_dnn_objdetect -lopencv_dnn_superres -lopencv_dpm -lopencv_face -lopencv_fuzzy -lopencv_hfs -lopencv_img_hash -lopencv_intensity_transform -lopencv_line_descriptor -lopencv_mcc -lopencv_quality -lopencv_rapid -lopencv_reg -lopencv_rgbd -lopencv_saliency -lopencv_shape -lopencv_stereo -lopencv_structured_light -lopencv_phase_unwrapping -lopencv_superres -lopencv_optflow -lopencv_surface_matching -lopencv_tracking -lopencv_highgui -lopencv_datasets -lopencv_text -lopencv_plot -lopencv_ml -lopencv_videostab -lopencv_videoio -lopencv_viz -lopencv_wechat_qrcode -lopencv_ximgproc -lopencv_video -lopencv_xobjdetect -lopencv_objdetect -lopencv_calib3d -lopencv_imgcodecs -lopencv_features2d -lopencv_dnn -lopencv_flann -lopencv_xphoto -lopencv_photo -lopencv_imgproc -lopencv_core

calibrate: src/calibration/calibration.cpp
	bear -- clang++ $(shell pkg-config --cflags opencv4) $(shell pkg-config --libs opencv4) -o $@ $^
CC = gcc
CFLAGS = -Wall -Wextra -std=c11

all: hello

hello: hello.c
	$(CC) $(CFLAGS) -o hello hello.c

run: hello
	./hello

clean:
	rm -f hello
