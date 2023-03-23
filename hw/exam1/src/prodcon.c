#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>

#define NUM_PRODUCERS 2
#define NUM_CONSUMERS 2
#define MESSAGE_SIZE 10
#define NUM_MESSAGES 2

char pid_str[10];
char random_string[MESSAGE_SIZE];
char *my_pid_as_string(void);
char *get_random_string(int);

void prod_code(int prod_id, int write_fd, int* con_pids)
{
	for (int i = 0; i<NUM_MESSAGES*NUM_CONSUMERS; i++){
		char* msg = get_random_string(prod_id);
		write(write_fd, msg, MESSAGE_SIZE);
	}
	close(write_fd);
	for (int i=0; i<NUM_CONSUMERS; i++){
			int status;
			waitpid(con_pids[i], &status, 0);
			int num_read=WEXITSTATUS(status);
			printf("Consumer %d (PID %d) consumed %d messages.\n",prod_id*10+i, con_pids[i], num_read);
	}
  printf("Producer %d (PID %s) finished.\n",prod_id, my_pid_as_string());
	exit(0);
}
void con_code(int con_id, int read_fd)
{
  printf("Consumer %d (PID %s) started.\n",con_id, my_pid_as_string());
  char buf[MESSAGE_SIZE];
	int numRead = 0;
	sleep(1);
  while(read(read_fd, buf, MESSAGE_SIZE)>0){
    printf("Consumer %d (PID %s) got string %s.\n",con_id, my_pid_as_string(), buf);
		numRead++;
	}
	close(read_fd);
  printf("Consumer %d (PID %s) finished.\n",con_id, my_pid_as_string());
	exit(numRead);
}

int main(int argc, char **argv)
{
  // Add your code here...
  printf("Master Process (PID %s) started.\n", my_pid_as_string());
  int a=1; //just in case it somehow doesn't reach init
  int producer_id=1;
	for (int j=0; j<NUM_PRODUCERS; j++){
			if (fork()==0){
					printf("Producer %d (PID %s) started.\n",producer_id+j, my_pid_as_string());
					int pipe_fd[2];
					int con_pids[NUM_CONSUMERS];
					pipe(pipe_fd);
					for (int i = 0; i<NUM_CONSUMERS; i++){
							a = fork();
							if (a==0){
									close(pipe_fd[1]);
									con_code(i+10*(j+1), pipe_fd[0]);
							}
							else{
									con_pids[i]=a;
							}
					}
					if (a!=0){
							close(pipe_fd[0]);
							prod_code(producer_id+j, pipe_fd[1], con_pids);
					}
			}
	}
	my_pid_as_string();
	int b = fork();
	if (b==0){
			execlp("pstree","pstree", "-p", pid_str, NULL);
			exit(1);
	}
	else{
			wait(NULL);//make sure that parent waits for pstree to finish
	}
	for (int i=0; i<NUM_PRODUCERS; i++){// wait for all of the producers
			wait(NULL);
	}
	printf("Master Process (PID %s) finished.\n", my_pid_as_string());
  
}

//////////////////////////////////////////////////////////////////////////////
// Please do not change any code below this point                           //
//////////////////////////////////////////////////////////////////////////////
char *my_pid_as_string(void)
{
  snprintf(pid_str, 10, "%d", getpid());
  return pid_str;
}

char *get_random_string(int producer)
{
  static int counter = 1;
  char *nouns[] = {"man", "cpu", "fan", "bot", "car", "can", "bug"};
  char *adjectives[] = {"big", "bad", "red", "fun", "hot", "hip", "icy", "new"};

  srand(getpid()*counter);
  counter++;
  snprintf(random_string, MESSAGE_SIZE, "%s %s %d",
           adjectives[rand()%8], nouns[rand()%7], producer);
  printf("Producer %d (PID %d) generated string '%s'.\n",
         producer, getpid(), random_string);
  return random_string;
}
