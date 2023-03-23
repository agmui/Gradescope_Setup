all: main.bin minionsay.bin


.PHONY: clean all
clean:
	rm -rf *.bin *.o
main.bin:main.o llist.o minionsay.bin
	gcc main.o llist.o -o main.bin
minionsay.bin: minionsay.o
	gcc minionsay.o -o minionsay.bin
llist.o: llist.c llist.h
	gcc -c llist.c llist.h 
main.o: main.c llist.h
	gcc -c main.c llist.h 
minionsay.o: minionsay.c
	gcc -c minionsay.c 
