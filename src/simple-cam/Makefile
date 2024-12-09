all:
	c++ -o simplecam $$(pkg-config --cflags libcamera) event_loop.cpp simple-cam.cpp $$(pkg-config --libs libevent_pthreads) $$(pkg-config --libs libcamera)
