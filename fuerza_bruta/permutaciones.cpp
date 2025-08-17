#include <iostream>
using namespace std;

class Solution{

    public:

        void permutacionesLex(int n){
            int p[n];
            int num_permutaciones = 0;
            for(int x = 0 ; x<n; x++){
                p[x] = x+1;
                std::cout << p[x] << "  " ;
            }
            std::cout << "\n";

            while(true){
                num_permutaciones ++;
                
                int i = n-2;
                int j = n-1;
                
                while(i>=0 && !(p[i] < p[i+1])){
                    i--;
                }

                if(i < 0) break;
                
                while(p[i] >= p[j]){
                    j--;
                }

                int temp = p[i];
                p[i] = p[j];
                p[j] = temp;
            
                int l = i + 1, r = n - 1;
                while(l < r){
                    int t = p[l];
                    p[l] = p[r];
                    p[r] = t;
                    l++; r--;
                }
                for(int y = 0 ; y<n; y++){
                    std::cout << p[y] << "  " ;
            }
            std::cout << "\n";
        }
        std::cout << "Permutaciones totales: " << num_permutaciones << "\n";
    }
};

        int main(){
            Solution per;
            per.permutacionesLex(3);
            return 0;
        }