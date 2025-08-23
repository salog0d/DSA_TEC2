/*
Fake Coin Problem (Divide and Conquer)

Description:
Dado un arreglo de monedas idénticas excepto una falsa con peso distinto (ejemplo: 1 frente a 0),
se busca la posición de la moneda falsa dividiendo el arreglo en tercios y comparando sumas.

ALGORITHM fake_coin(arr)
Input: arreglo de enteros (0 = moneda real, 1 = falsa en este ejemplo)
Output: índice de la moneda falsa

- Complejidad aproximada: O(log n) si se divide en 3 partes de manera recursiva
- Complejidad actual: O(n) por los bucles de suma + búsqueda lineal
*/

#include <iostream>
#include <vector>
using namespace std;

class Solution{

    public:

    void fake_coin(vector<int> arr){

        int n= (int)arr.size();
        if(n<=0){
            std:cout << "Ingrese un arreglo valido";
            return;
        }
        
        int l = n-1;
        int k = l/3;
        int j = 0;
        int sum1=0;
        int sum2=0;
        int real_sum = 0;
        int real_coin = 0;
        int fake_coin = 0;

        for(int i=0; i<l;i++){
            if(i<=k){
                sum1 += arr[i];
            }
            else if(i>k && i<=2*k){
                sum2 += arr[i];
            }
        }

        if(sum1==sum2){
            j = 2*k+1;
            real_coin = arr[0];
        }
            else{
                real_coin = arr[2*k+1];
                real_sum = real_coin*k;
        }

        if(real_sum==sum1){
            j = k+1;
        }

        while(true){
            if(real_coin != arr[j]){
                fake_coin = j;
                break;
            }
            j++;
        }

        std::cout<<"Fake coin is in index: " << fake_coin;
    }
};

int main(){
    Solution sol;

    vector<int> arr = {0,0,0,0,0,0,1,0,0,0,0,0,0,0};
    sol.fake_coin(arr);

}
