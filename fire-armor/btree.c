#include <stdio.h>
#include <stdlib.h>

#define btree_max 3
#define btree_min 2

typedef struct node_s
	int val[bree_max+1], cnt;
	struct node_s *link[bree_max+1];
} node_t;

struct nodes_s root;

void insert(int val);



node_t * make_node(int val, node_t *child);
void insert_node(int val, int pos, node_t node);
void split_node(int val, int *pval, int pos, node_t *node, node_t *child, node_t new_node);
int set_value(int val, int *pval, 



