SOURCES := problem3.c problem4_child.c problem4_parent.c
TARGETS := $(SOURCES:%.c=%.bin)

all: $(TARGETS)

CC = gcc
CFLAGS += -ggdb -Werror -O0 -fno-builtin-puts -Wl,--wrap=printf,--wrap=puts,--wrap=putchar,--wrap=fork
LDFLAGS += -lm

.PHONY: clean all

%.bin: %.o exam.h
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

clean:
	rm -rf *.o *.bin *.log

