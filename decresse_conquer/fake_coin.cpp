#include <iostream>
using namespace std;

class Solution{

    public:

    void fake_coin(int *arr, int length){
        if(length<=0){
            std:cout << "Ingrese un arreglo valido";
            return;
        }
        
        int divisions = 0;
        if(length%2==0){
            divisions = 2;
        }
        else{
            divisions = 3;
        }
        
        int val1= 0;
        int val2=0;
        int val3=0;

        for(int i=0; i<length;i++){
            int chunks_size = length/divisions;
            int remainigs[0];
            if(i < chunks_size){

            }
            else if(i < 2*chunks_size){

            }
            else if(i < 3*chunks_size && divisions==3){

            }
        }
        
            
    }

};