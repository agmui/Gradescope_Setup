#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

int thread_num;
pthread_mutex_t mutex;
pthread_cond_t c;


void *thread(void *arg)
{
	char *letter = (char *)arg;
	printf("%c wants to enter the critical section\n", *letter);

	pthread_mutex_lock(&mutex);
	while(thread_num>2){
        pthread_cond_wait(&c,&mutex);
    }
	thread_num++;
	pthread_mutex_unlock(&mutex);

	printf("%c is in the critical section\n", *letter);
	sleep(1);
	pthread_mutex_lock(&mutex);
	thread_num--;
	pthread_mutex_unlock(&mutex);
	printf("%c has left the critical section\n", *letter);
	pthread_cond_signal(&c);
	return NULL;
}

int
main(int argc, char **argv)
{
	thread_num = 0;
    pthread_mutex_init(&mutex, 0);
        
	pthread_t threads[8];
	int i;
	char *letters = "abcdefgh";

	for(i = 0; i < 8; ++i) {
		pthread_create(&threads[i], NULL, thread, &letters[i]);

		if(i == 4)
			sleep(4);
	}

	for(i = 0; i < 8; i++) {
		pthread_join(threads[i], NULL);
	}

	printf("Everything finished...\n");

	return 0;
}
