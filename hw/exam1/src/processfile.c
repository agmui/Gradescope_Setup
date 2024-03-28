#include "exam.h"

// You should not need to edit this file

int main(int argc, char** argv) {
    srand(getpid());

    if(argc < 2) {
        printf("processfile needs to be passed a filename\n");
        exit(1);
    }
    printf("processfile PID %d starting work on file %s\n", getpid(), argv[1]);
    sleep(1);
    int result = rand() % 3;
    if(result != 0) {
        printf("processfile PID %d SUCCESS on file %s\n", getpid(), argv[1]);
        exit(0);
    } else {
        printf("processfile PID %d FAILURE on file %s\n", getpid(), argv[1]);
        exit(2);
    }

}
