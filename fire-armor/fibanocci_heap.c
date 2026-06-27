
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>


typedef struct node_s {
	int val, degree;
	struct node_s *prev, *next;
	struct node_s *parent, *child;
	bool mark, visited;
} node_t;
typedef struct fibanocci_heap_s {
	int n, phi, degree;
	node_t *min;
} fibanocci_heap_t;

// make a fibanocci heap
fibanocci_heap_t *make_fibanocci_heap();

// inserting a node
void insertion(int val, node_t *out, fibanocci_heap_t *fh);

node_t *extract_min(fibanocci_heap_t fh);

void consolidate(fibanocci_heap_t *fh);

fibanocci_heap_t *make_fibanocci_heap()
{
	fibanocci_heap_t *fh;
	fh = (fibanocci_heap_t *) malloc(sizeof(fibanocci_heap_t));
	fh->n = 0;
	fh->min = NULL;
	fh->phi = 0;
	fh->degree = 0;
	return fh;
}

void print_heap(node_t *x) 
{
	node_t *y;
	for(y = x;;  x->next) {
		if(x->child == NULL) {
			printf("node with no child (%d)\n", y->val);
		} else {
			print_heap(x->child);
		}
		if (y ->next == x) {
			break;
		}
	}
}

void insertion(int val, node *out, fibanocci_heap_t *fh) 
{
	out = (node_t *) malloc(sizeof(node_t));
	out->val = val;
	out->degree = 0;
	out->mark = false;
	out->visited = false;
	out->parent = NULL;
	out->child = NULL;
	out->next = out;
	out->prev = out;
	if (fh->min == NULL) 
	{
		fh->min = out;
	} 
	else 
	{
		h->min->prev->next = out;
		out->next = fh->min;
		out-prev = fh->min->prev;
		h->min->prev = out;
	}
	(fh->n)++;
}

int main(void) {
	printf("test fibanocci_heap\n");
	return 0;
}

