#include<iostream>
#include<sstream>

#include<algorithm>
#include<functional>
#include<vector>
#include<deque>
#include<map>

#include<cstdio>
#include<cstring>

using namespace std;

int main(){
    int n; cin >> n;
    for(auto i = 0; i < n; i++) {
        int m; cin >> m;
        vector<int> p(m);
        for(int j = 0; j < m; j++) cin >> p[j];
        int j = 0;
        for(; j < m && p[j] == m-j; j++);
        if (j < m) {
            int k = j;
            for(; k < m && p[k] != m-j; k++);
            auto it = p.begin();
            reverse(it+j, it+k+1);
        }
        for(auto it = p.begin(); it != p.end(); it++) {
            cout << *it << " ";
        }
        cout << endl;
    }
}
