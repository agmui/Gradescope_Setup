#include <assert.h>

#include "llist.h"

void init_list(struct node *n)
{
	n->next = n->prev = 0;
}

void append_list(struct node *n, struct node *new)
{
	assert(!n->next);

	init_list(new);
	n->next = new;
	new->prev = n;
}

void print_list(struct node *n, void (*print_fn)(void *d))
{
	struct node *it = n;

	while(it) {
		print_fn(it->data);
		it = it->next;
	}
}
