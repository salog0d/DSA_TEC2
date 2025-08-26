/*
Complejidad O(n*K)
Donde n es el numero de monedas y K es el valor de el cambio.
*/

#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    long long coinChange(int n, int K, const vector<int>& C){
        
        vector<vector<int>> M(n + 1, vector<int>(K + 1, 0));
        M[0][0] = 1; 
        
        if(K==0){
            return  M[0][0];
        }

        

        for(int i = 1; i <= n; ++i){
            for(int j = 0; j <= K; ++j){
                M[i][j] += M[i-1][j];
                if(j - C[i-1] >= 0){
                    M[i][j] += M[i][j - C[i-1]];
                }
            }
        }
        return M[n][K];
    }
};

int main(){
    Solution sol;

    int n = 4;
    vector<int> C = {1, 2, 5, 10};
    int K = 0;

    long long result = sol.coinChange(n, K, C);
    cout << result << '\n';
}