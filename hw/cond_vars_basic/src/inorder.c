#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

int thread_num;
pthread_mutex_t mutex;
pthread_cond_t c;

void *thread(void *arg)
{
        int *num = (int *)arg;

        pthread_mutex_lock(&mutex);
        printf("%d wants to enter the critical section\n", *num);
        while(thread_num!=*num){
                pthread_cond_wait(&c,&mutex);
        }
        thread_num++;
	printf("%d is in the critical section\n", *num);

        printf("%d is finished with the critical section\n", *num);
        pthread_mutex_unlock(&mutex);
        pthread_cond_signal(&c);
        return NULL;
}

int
main(int argc, char **argv)
{
        thread_num = 1;
        pthread_mutex_init(&mutex, 0);
        pthread_t threads[4];
        int i;
        int nums[] = {2, 1, 4, 3};

        for(i = 0; i < 4; ++i) {
                pthread_create(&threads[i], NULL, thread, &nums[i]);

                if(i == 2)
                        sleep(3);
        }

        for(i = 0; i < 4; ++i) {
                pthread_join(threads[i], NULL);
        }
        pthread_mutex_destroy(&mutex);
        printf("Everything finished\n");

        return 0;
}