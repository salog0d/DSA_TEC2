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
#include <cstdlib>
#include <ctime>
using namespace std;

class Solution{
    public:
    void fake_coin(int n){
        if(n <= 0){
            cout << "Ingrese un tamaño válido" << endl;
            return;
        }

        srand(time(0));
        vector<int> arr(n,0);
        int fake_index = rand() % n;
        arr[fake_index] = 1;

        
        int l = n-1;
        int k = l/3;
        int j = 0;
        int sum1=0, sum2=0, real_sum = 0, real_coin = 0;
        int fake_coin = -1;

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

        while(j<n){
            if(real_coin != arr[j]){
                fake_coin = j;
                break;
            }
            j++;
        }

        cout<<"Moneda falsa detectada en índice: " << fake_coin << endl;
    }
};

int main(){
    Solution sol;
    int n;
    cout << "Ingrese el tamaño del arreglo de monedas: ";
    cin >> n;
    sol.fake_coin(n);
}
