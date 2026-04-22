#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <limits.h>
#include <stdbool.h>
#include <assert.h>

void print_iarray(char *prefix, int *a, int n) {
	int m = 1000;
	char buf[m]; 
	char *s = buf;
	char *e = s; 
	int i;
	for(i = 0; i < n; i++) {
		e += sprintf(e, i < n-1 ? "%2d " : "%2d", i);
	}
	printf("%s- %s ---index\n", prefix, s);
	s = e;
	for(i = 0; i < n; i++) {
		e += sprintf(e, i < n-1 ? "%2d " : "%2d", *(a+i));
	}
	printf("%s-[%s]\n", prefix, s);
}

int abs(int a) { if (a >= 0) return a;  return -a; }
int comparator(const void *a, const void *b) { return *(int *)a - *(int *)b; }
// https://codeforces.com/problemset/problem/2111/C
// https://onlinejudge.org/external/4/p455.pdf
// https://codeforces.com/problemset/problem/2106/C

int main() {
    
}

