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
            if(k < 1 || k > n){
                std::cout<<"Target index out of bounds";
                return;
            }

            int s = 0;
            int l = n - 1;
            int target = k - 1;

            while(true){
                int pivot = nums[s];
                int i = s + 1;

                for(int j = s + 1; j <= l; j++){
                    if(nums[j] < pivot){
                        swap(nums[i], nums[j]);
                        i++;
                    }
                }

                int pivotIndex = i - 1;
                swap(nums[s], nums[pivotIndex]);

                if(pivotIndex == target) {
                    cout << "El valor en la posición " << k << " es " << nums[pivotIndex] << endl;
                    break;
                }
                else if(pivotIndex > target){
                    l = pivotIndex - 1;
                }
                else {
                    s = pivotIndex + 1;
                }
            }
        }
};

int main(){
    Solution sol;
    vector<int> nums = {6,1,24,4,5,7,2,8,9};

    sol.quick_select(nums, 5);
    return 0;
}
