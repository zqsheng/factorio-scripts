#include<stdio.h>

void print_iarray(char *prefix, int *a, int n) {
	int m = 1000;
	char buf[m]; // start
	char *s = buf;
	char *e = s; // end
	for(int i = 0; i < n; i++) {
		e += sprintf(e, i < n-1 ? "%2d " : "%2d", i);
	}
	printf("%s-[%s]\n", prefix, s);
	s = e;
	for(int i = 0; i < n; i++) {
		e += sprintf(e, i < n-1 ? "%2d " : "%2d", *(a+i));
	}
	printf("%s-[%s]\n", prefix, s);
}



int min(int a, int b) { if (a < b)  return a; return b; }
int max(int a, int b) { if (a > b)  return a; return b; }

int lowbit(int x) { return x & -x; }

// warning, error if x < 0 
// fixed, return x - ((unsigned int) x >> 1);
int highbit(int x) {
	x |= x >> 1;
	x |= x >> 2;
	x |= x >> 4;
	x |= x >> 8;
	x |= x >> 16;
	return x - (x >> 1); 
}

// todo
int Inf = 999999;


void build_bit(int *a, int n,  int *bit1, int *bit2) {
	for(int i = 1; i <= n; i++) {
		bit1[i] = a[i]; 
		bit2[i] = a[i]; 
	}
	bit1[n+1] = Inf;
	bit2[0] = Inf;
	for(int i = 1; i <= n; i++) {
		for(int j = i, p = j + lowbit(j); p <= n + 1; j = p, p = j + lowbit(j)) {
			bit1[p] = min(bit1[p], bit1[j]);
//			printf("%d %d %d\n",i, j, p);
		}
		for(int j = i, p = j - lowbit(j); ; j = p, p = j - lowbit(j)) {
			bit2[p] = min(bit2[p], bit2[j]);
			// printf("%d %d %d\n",i, j, p);
			if (p == 0) break;
		}
	}
	print_iarray("bit1", bit1, n + 2);
	print_iarray("bit2", bit2, n + 2);
}

int query(int l, int r, int *a, int n, int *bit1, int *bit2) {
	// todo
	// compute exact
	// 5    0101
	//13    1101
	int k = l;
	if (l < r) {
		int s = l, e = r;
		for(int sh = highbit(s), eh = highbit(e); sh == eh; s -= sh, e -= sh);
		k = max(highbit(s), highbit(e));
		printf("k: %d %d %d\n", l, r, k);
	}

	int res = a[l];
	for(int i = l, p = i + lowbit(i); p <= k; i = p, p = i + lowbit(i)) {
		res = min(res, bit1[i]);
		res = min(res, bit1[p]);
		printf("climbing left tree: %d %d\n", i, p);
	}
	
	for(int i = r, p = i - lowbit(i); p >= k; i = p, p = i - lowbit(i)) {
		res = min(res, bit1[i]);
		res = min(res, bit1[p]);
		printf("climbing right tree: %d %d\n", i, p);
	}
	return res;
}
void update(int i, int v, int *a, int n, int *bit1, int *bit2) {
	a[i] = v;
	int l = i - lowbit(i) + 1; 
	bit1[i] = min(query(l, i, a, n, bit1, bit2), v);
	for(int j = i, p = j + lowbit(j); p <= n + 1; j = p, p = j + lowbit(j)) {
		bit1[p] = min(bit1[p], bit1[j]);
	}
	int r = i + lowbit(i) - 1;
	bit2[i] = min(query(i + 1, r, a, n, bit1, bit2), v);
	for(int j = i, p = j - lowbit(j); ; j = p, p = j - lowbit(j)) {
		bit2[p] = min(bit2[p], bit2[j]);
		if (p == 0) break;
	}
	print_iarray("bit1", bit1, n + 2);
	print_iarray("bit2", bit2, n + 2);
}

void test() {
	int n = 15;
	// index 0 is invalid
	int a[] = {-1, 1, 0, 2, 1, 1,3,0,4,2,5,2,2,3,1,0}; 
	// index 0 is invalid, index n + 1 is root
	int bit1[n+2];
	// index n+1 invalid, index 0 is root
	int bit2[n+2];
	build_bit(a, n, bit1, bit2);
	int l = 5, r = 13;
	int res = query(l, r, a, n, bit1, bit2);
	printf("res: %d %d %d\n", l, r, res);
	update(5, -1, a, n, bit1, bit2);
	res = query(l, r, a, n, bit1, bit2);
	printf("res: %d %d %d\n", l, r, res);
}

int main() {
	test();
	return 0;
}
