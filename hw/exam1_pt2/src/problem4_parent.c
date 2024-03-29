#include "exam.h"

void main(){
    int pid = fork();
    if(pid==0){
      execlp("./problem4_child.bin", "./problem4_child.bin", NULL);
      exit(1);
    }
    wait(0);
}


