/*
String Matching (Brute Force)

Description:
Searches for multiple target patterns inside a text using brute force.
Each pattern is compared character by character against every possible
substring of the text. Counts and reports the number of times each 
pattern appears.

ALGORITHM stringMatching(targets[], text, targets_size)
Searches for each target string inside the given text
Input: array of target strings, text string, number of targets
Output: Number of repetitions of each target in the text

- Time complexity:  O(m * n) where m = text length, n = total length of all target patterns.
*/


#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
using namespace std;

class Solution{
public:

    void stringMatching(string targets[], string text, int targets_size){
        int text_size = text.length();
        
        for(int z=0; z< targets_size ; z++){
            int repetitions = 0;
            bool match = false;
            string target = targets[z];
            int target_size = targets[z].length();
            if (target_size == 0){
                std::cout << "Target is empty\n";
                return;   
            }
        
            if (target_size > text_size){
                std::cout << "Target size is greater than the text!\n";
                return;
            }
        
            for (int i = 0; i <= text_size - target_size; i++){
                int j = 0;
                int x = i;

                while (j < target_size && x < text_size && target[j] == text[x]){
                    j++;
                    x++;
                }
        
                if (j == target_size){
                    repetitions++;
                    match = true;
                }
            }
            
            if(match){
                std::cout << "The word " << target << " appears " << repetitions << " times in the text.\n";
            }
            else{
                std::cout << target << " is not in the text\n";
            }
        }
    }
};

int main() {
    Solution sol;

    
    std::ifstream text("fuerza_bruta/test_cases/string_matching/string-matching-Texto.txt");
    if(!text){
        std::cerr << "Error opening text file\n";
        return 1;
    }
    std::stringstream buffer;
    buffer << text.rdbuf();
    std::string textContent = buffer.str();

    std::ifstream targetsFile("fuerza_bruta/test_cases/string_matching/string-matching-Patrones.txt");
    if(!targetsFile){
        std::cerr << "Error opening targets file\n";
        return 1;
    }

    int MAX_TARGETS = 7;         
    std::string targets[MAX_TARGETS];   
    std::string line;
    int count = 0;


    while (std::getline(targetsFile, line) && count < MAX_TARGETS) {
        if (!line.empty()) {
            if (!line.empty() && line.back() == '\r') line.pop_back(); 
            targets[count] = line;
            count++;
        }
    }
    int targets_size = count; 


    sol.stringMatching(targets, textContent, targets_size);

    return 0;
}