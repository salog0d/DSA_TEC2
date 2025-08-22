#include <iostream>
#include <vector>
#include <queue>
using namespace std;

class Solution {

    public:

    vector<int> topologicalSort(vector<vector<int>> G){
        vector<int> n_order;
        n_order.push_back(0);                 

        if (G.empty()) return n_order;

        int columns = (int)G.size();

        for (int i = 0; i < columns; i++) {
            if(G[i]==0){
                n_order.push_back(G[i]);
            }
        return n_order;
    }
};

int main(){
    Solution sol;

    vector<vector<int>> G = {
    {1,2},  
    {3},    
    {3,4},  
    {},     
    {}      
};

    vector<int> n_order = sol.topologicalSort(G);
    int n = (int)n_order.size();          
    for (int i = 0; i < n; i++) {
        cout << n_order[i] << " ";
    }
};