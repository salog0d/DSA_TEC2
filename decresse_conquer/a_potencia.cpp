/*
a^n usando Exponenciación Rápida (Divide y Vencerás)

Descripción:
Implementa una función recursiva que calcula la potencia de un número entero
utilizando el método de exponenciación rápida. En lugar de multiplicar `a`
por sí mismo `n` veces (O(n)), divide el problema en subproblemas reduciendo
el exponente a la mitad en cada paso.

ALGORITHM a_potencia(a, n)
Input: base entera a, exponente entero no negativo n
Output: valor de a^n

- Si n == 0: retornar 1 (caso base).
- Si n es par:
    calcular y = a^(n/2)
    retornar y * y
- Si n es impar:
    calcular y = a^(n/2)
    retornar y * y * a

- Complejidad temporal: O(log n) (división sucesiva del exponente).
- Complejidad espacial: O(log n) por la pila de recursión.
*/


#include <iostream>
using namespace std;

class Solution{

    public:

        int a_potencia(int a , int n){
            int result = 1;
            int y=0;
            if(n==0){
                return result;
            }
            if(n%2==0){
                y=a_potencia(a,n/2);
                return y*y;
            }
            else{
                y=a_potencia(a,n/2);
                return y*y*a;
            }
        }
};

int main(){
    Solution sol;

    int result = sol.a_potencia(2,4);

    std::cout<< result ;
}
