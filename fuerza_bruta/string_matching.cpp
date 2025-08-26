/*
String Matching (Brute Force)

Description:
Searches for multiple target patterns inside a text using brute force.
Each pattern is compared character by character against every possible
substring of the text. Counts and reports the number of times each 
pattern appears, and prints the start/end indices (0-based) for each match.

ALGORITHM stringMatching(targets[], text, targets_size)
Searches for each target string inside the given text
Input: array of target strings, text string, number of targets
Output: Number of repetitions of each target in the text and their [start, end] indices

- Time complexity:  O(m * n) where m = text length, n = total length of all target patterns.
*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

class Solution{
public:
    void stringMatching(string targets[], string text, int targets_size){
        int text_size = (int)text.length();
        
        for (int z = 0; z < targets_size; z++){
            string target = targets[z];
            int target_size = (int)target.length();

            if (target_size == 0){
                cout << "Target is empty\n";
                continue;   
            }
            if (target_size > text_size){
                cout << "Target size is greater than the text!\n";
                continue;
            }

            int repetitions = 0;
            vector<pair<int,int>> positions; // [start, end] for each match (0-based)

            for (int i = 0; i <= text_size - target_size; i++){
                int j = 0;
                int x = i;

                while (j < target_size && x < text_size && target[j] == text[x]){
                    j++;
                    x++;
                }
                if (j == target_size){
                    repetitions++;
                    positions.emplace_back(i, i + target_size - 1);
                }
            }
            
            if (!positions.empty()){
                cout << "The word \"" << target << "\" appears " << repetitions << " times.\n";
                cout << "Positions (start,end) 0-based: ";
                for (size_t k = 0; k < positions.size(); k++){
                    cout << "[" << positions[k].first << "," << positions[k].second << "]";
                    if (k + 1 < positions.size()) cout << " ";
                }
                cout << "\n";
            } else {
                cout << "\"" << target << "\" is not in the text\n";
            }
        }
    }
};

int main() {
    Solution sol;

    ifstream text("fuerza_bruta/test_cases/string_matching/string-matching-Texto.txt");
    if(!text){
        cerr << "Error opening text file\n";
        return 1;
    }
    stringstream buffer;
    buffer << text.rdbuf();
    string textContent = buffer.str();

    ifstream targetsFile("fuerza_bruta/test_cases/string_matching/string-matching-Patrones.txt");
    if(!targetsFile){
        cerr << "Error opening targets file\n";
        return 1;
    }

    const int MAX_TARGETS = 7;         
    string targets[MAX_TARGETS];   
    string line;
    int count = 0;

    while (getline(targetsFile, line) && count < MAX_TARGETS) {
        if (!line.empty()) {
            if (!line.empty() && line.back() == '\r') line.pop_back(); 
            targets[count++] = line;
        }
    }
    int targets_size = count; 

    sol.stringMatching(targets, textContent, targets_size);
    return 0;
}
