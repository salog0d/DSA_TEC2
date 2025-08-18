#include <iostream>
using namespace std;

class Solution{

    public:

    bool twoSum(int k, int c[],int length){
        for(int i=0;i<length;i++){
            for(int j=i; j<length;j++){
                if(c[i]+c[j]==k){
                    return true;
                }
            }
        }
        return false;
    }
};

int main(){

    Solution sol;

    int arr[5] = {1,3,5,2,6};
    int length = sizeof(arr) / sizeof(arr[0]);
    int k = 7;
    bool sum = sol.twoSum(k,arr,length);
    if(sum)
        std::cout << "There are two pairs that sum " << k ;
    else
        std::cout << "TNo pairs sum " << k ;
    return 0;
}