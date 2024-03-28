
all: processfile.bin processbatch.bin

processfile.bin: processfile.c exam.h
	gcc  -O0 -fno-builtin-puts -Wl,--wrap=printf,--wrap=puts,--wrap=putchar,--wrap=fork -o processfile.bin processfile.c

processbatch.bin: processbatch.c exam.h
	gcc  -O0 -fno-builtin-puts -Wl,--wrap=printf,--wrap=puts,--wrap=putchar,--wrap=fork -o processbatch.bin processbatch.c

