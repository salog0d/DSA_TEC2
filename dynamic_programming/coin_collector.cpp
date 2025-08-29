/*
Complejidad O(n*m)
Donde n es la altura y m el ancho de la matriz C.
*/

#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
using namespace std;

class Solution{

public:

    int coinCollector(vector<vector<int>> &C){
        int n = (int)C.size();
        if(n == 0) return 0;
        int m = (int)C[0].size();
    
        vector<vector<int>> A(n, vector<int>(m, 0));
    
        A[0][0] = C[0][0];
    
        for(int i = 1; i < n; i++){
            A[i][0] = A[i-1][0] + C[i][0];
        }
    
        for(int j = 1; j < m; j++){
            A[0][j] = A[0][j-1] + C[0][j];
        }
    
        for(int i = 1; i < n; i++){
            for(int j = 1; j < m; j++){
                A[i][j] = max(A[i-1][j], A[i][j-1]) + C[i][j];
            }
        }
        return A[n-1][m-1];
    }

};

// Función auxiliar para leer la matriz desde archivo
vector<vector<int>> leerMatrizDesdeArchivo(const string& filename){
    ifstream file(filename);
    if(!file.is_open()){
        cerr << "No se pudo abrir el archivo " << filename << endl;
        exit(1);
    }

    string line;
    vector<vector<int>> matriz;
    bool skipFirst = true; // saltar primera línea

    while(getline(file, line)){
        if(skipFirst){ skipFirst = false; continue; }

        stringstream ss(line);
        int num;
        vector<int> fila;
        while(ss >> num){
            fila.push_back(num);
        }
        if(!fila.empty()) matriz.push_back(fila);
    }

    return matriz;
}

int main() {
    Solution sol;
    vector<string> archivos = {
        "test_cases/coins-n5.txt",
        "test_cases/coins-n10.txt",
        "test_cases/coins-n20.txt",
        "test_cases/coins-n100.txt"
    };

    for (const string& archivo : archivos) {
        vector<vector<int>> C = leerMatrizDesdeArchivo(archivo);
        int result = sol.coinCollector(C);
        cout << archivo << " -> Resultado: " << result << endl;
    }

    return 0;
}
