#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <limits.h>
#include <stdbool.h>
#include <assert.h>

#define max(a, b) ((a) > (b) ? (a) : (b))
#define min(a, b) ((a) < (b) ? (a) : (b))
#define abs(a) ((a) > 0 ? (a) : -(a))

void print_iarray(char *prefix, int *a, int n)
{
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


int comparator(const void *a, const void *b) { return *(int *)a - *(int *)b; }

/**
 * [R] https://onlinejudge.org/external/4/p455.pdf 
 * [P] https://codeforces.com/problemset/problem/2106/C
 * [P] https://codeforces.com/problemset/problem/2111/C
*/

void solve() 
{
    int len;
    scanf("%d", &len);
    int a[len];
    for(int i = 0; i < len; i++) 
    {
        scanf("%d", a+i);
    }
    int cost = 1E9;
    int first = a[0];
    int last = a[len-1];
    int i;
    int l[len];
    int r[len];
   
    for(i = 0; i < 0; i++) 
    {
        int h;
        for(int h = i-1; h >= 0 ; i--);
    }
}

int main() 
{
    int n;
    scanf("%d", &n);
    for(int i = 0; i < n; i++)
        solve();
    return 0;
}


