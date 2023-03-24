#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

#include "llist.h"

#define PROGRAM_NAME "./minionsay.bin"
#define MESSAGE "Hello! I am a sitting duck\n"

void print_fn(void *d)
{
	int x = *((int*)d);
	printf("Element %d\n", x);
}

void duckduckgo(void)
{
	if(fork() == 0) {
		execlp(PROGRAM_NAME, PROGRAM_NAME, MESSAGE, 0);
		perror("Exec failed");
		exit(1);
	}
	wait(0);
}

int main()
{
	struct node *head, *n;
	int x = 3, y = 4;

	duckduckgo();

	head = malloc(sizeof(struct node));
	init_list(head);
	head->data = &x;

	n = malloc(sizeof(struct node));
	init_list(n);
	n->data = &y;

	append_list(head, n);
	print_list(head, print_fn);

	free(head); head = 0;
	free(n); n = 0;

	exit(0);
}
