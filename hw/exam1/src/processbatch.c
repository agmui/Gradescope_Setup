#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>

int main(int argc, char** argv) {

    int pids[argc];
    
    if(argc < 2) {
        printf("you must pass at least one file parameter\n");
    }

    for(int i = 1; i < argc; i++) {
        printf("parent %d ready to process %s\n", getpid(), argv[i]);
        int waiter = fork();
        if (waiter == 0) {
            int status = 1;
            while (status != 0) {
                int result = fork();
                if (result == 0) {
                    execlp("./processfile.bin", "./processfile.bin", argv[i], NULL);
                }
                wait(&status);
                if (status != 0) {
                    printf("restarting processfile for %s\n", argv[i]);
                }
            }
            exit(0);
        }
    }
    for (int i = 1; i < argc; i++) {
        wait(NULL);
    }

    printf("parent %d done\n", getpid());
}
