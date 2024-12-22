CPPFLAGS = -Wall -Wextra -Wpedantic -Werror -Wfatal-errors# -Wconversion

simplecam:	simple-cam.o event_loop.o
	clang++ $(CPPFLAGS) -o $@ $^ $$(pkg-config --libs libevent_pthreads) $$(pkg-config --libs libcamera)
	sed -e '1s/^/[\n/' -e '$$s/,$$/\n]/' *.o.json > compile_commands.json

%.o:	%.cpp
	clang++ $(CPPFLAGS) -c -MJ $@.json -o $@ $$(pkg-config --cflags libcamera) $^

.PHONY: 	clean

clean:
	rm -f *.o *.o.json simplecam compile_commands.json
