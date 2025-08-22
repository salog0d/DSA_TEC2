#include <iostream>
#include <vector>
using namespace std;

class Solution {

    public:
        void quick_select(vector<int> nums, int k){
            int n = nums.size();

            if(nums.empty()){
                std::cout<< "El arreglo esta vacio";
                return;
            }
            if(k<n||k>n){
                std::cout<<"Target index out of bounds";
                return;
            }

            int s = 0;
            int l = n-1;
            int k = k-1;
            while(true){
                int pivot = nums[0];
                for(int i=0; i<l; i++){
                    if(nums[i]<=pivot){
                        int temp = nums[i];
                        nums[i] = nums[s];
                        nums[s] = temp;
                        s++;
                    }
                }
                if (s== k) {
                    cout << "El valor en la posición " << k << " es " << pivot << endl;
                    break;
                }
                else if(s>k){
                    division=s;
                }
                else if(s<k){
                    i= s+1;
                }
            }
        }
};

int main(){
    Solution sol;
    vector<int> nums = {6,1,24,4,5,7,2,8,9};

    sol.quick_select(nums,1);

    return 0;
}