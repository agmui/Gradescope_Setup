SOURCES := problem1.c problem2.c problem3.c
TARGETS := $(SOURCES:%.c=%.bin)

all: $(TARGETS)

CC = gcc
CFLAGS += -ggdb -Werror -Wall -O0 -fno-builtin-puts -Wl,--wrap=printf,--wrap=puts,--wrap=putchar,--wrap=fork
LDFLAGS += -lm -pthread

.PHONY: clean all

%.bin: %.o exam.h
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

clean:
	rm -rf *.o *.bin *.log

