#ifndef __LLIST_H
#define __LLIST_H

struct node {
	void *data;
	struct node *prev, *next;
};

void init_list(struct node*);

void append_list(struct node*, struct node*);

void print_list(struct node*, void (*)(void*));

#endif
