/*
Complejidad O(n*m)
Donde n es la altura y m el ancho de la matriz C.
*/

#include <iostream>
#include <vector>
using namespace std;

class Solution{

    public:

        int coinCollector(vector<vector<int>> &C){
            int n = (int)C.size();
            if(n == 0) return 0;
            int m = (int)C[0].size();
        
            vector<vector<int>> A(n, vector<int>(m, 0));
        
        
            A[0][0] = C[0][0];
        
        
            for(int i = 1; i < n; i++){
                A[i][0] = A[i-1][0] + C[i][0];
            }
        
            for(int j = 1; j < m; j++){
                A[0][j] = A[0][j-1] + C[0][j];
            }
        
        
            for(int i = 1; i < n; i++){
                for(int j = 1; j < m; j++){
                    A[i][j] = max(A[i-1][j], A[i][j-1]) + C[i][j];
                }
            }

            return A[n-1][m-1];
    }


};

int main(){
    Solution sol;

    vector<vector<int>> C = {
        {5, 0, 0},
        {0, 2, 0},
        {1, 1, 1}
    };

    int result = sol.coinCollector(C);
    cout << "Resultado: " << result << endl;

    return 0;
}