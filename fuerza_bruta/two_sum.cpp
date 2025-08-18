/*
Algorithm selected: Two sum
This is the version of the problem two sum using brute force, each element compares
itself to all the elements on the list until the program finds a subset of two elements 
that satisfy (sum elements == target)

Pseudocode

ALGORITHM twoSum(k,C,l)
Searches for the sum k of two elements of the set 'c' with length l
Input: Array C, size l and value k
Output: True if there is a pair of values that sum k and false if not

for i = 0 to l
    for j = i to l
        if C[i]+C[j] == k
            return true
        end if 
    end for 
end for 
return false

*/

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