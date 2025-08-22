#include <iostream>
#include <vector>
using namespace std;

class Solution {

    public:

    vector<int> topologicalSort(vector<vector<int>> G){
    vector<int> n_order;
    n_order.push_back(0);                 

    if (G.empty()) return n_order;

    int columns = (int)G.size();

    for (int i = 0; i < columns; ++i) {
        for (int u = 0; u < (int)G[i].size(); ++u) {
            n_order.push_back(G[i][u]);
        }
    }
    return n_order;
}
};

int main(){
    Solution sol;

    vector<vector<int>> G = {
        {1,2,6,4},
        {5},
        {3,3,2,6},
        {100,40},
        {}         
    };

    vector<int> n_order = sol.topologicalSort(G);
    int n = (int)n_order.size();          
    for (int i = 0; i < n; i++) {
        cout << n_order[i] << " ";
    }
};