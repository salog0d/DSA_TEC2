#include <iostream>
#include <vector>
using namespace std;

class Solution {

    public:
        void quick_select(vector<int> nums, int s){
            int n = nums.size() -1 ;

            if(nums.empty()){
                std::cout<< "El arreglo esta vacio";
                return;
            }
            if(n<s){
                std::cout<<"Target index out of bounds";
                return;
            }

            int division = n;
            while(true){
                vector<int> temp;
                int pivot = nums[0];
                int swaps = 0;
                for(int i= 1; i<division; i++){
                    if(nums[i]<=pivot){
                        temp.push_back(nums[i]);
                        swaps ++;
                    }
                }
                if (swaps == s) {
                    cout << "El valor en la posición " << s << " es " << pivot << endl;
                    break;
                }

                division = swaps;
            }
        }
};

int main(){
    Solution sol;
    vector<int> nums = {6,1,24,4,5,7,2,8,9};

    sol.quick_select(nums,1);

    return 0;
}