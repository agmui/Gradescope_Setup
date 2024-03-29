#include "exam.h"

void child();

int main(int argc, char** argv){
  child();
}

void child(){
  unsigned int h;
  printf("Child:\n");
  printf("Enter a length: ");
  scanf("%d", &h);
  
  srandom(h);

  for(int i=0; i<h; i++){
      char c = 'A'+(random()%2);
      printf("%c", c);
  }
  printf("\n");
}

