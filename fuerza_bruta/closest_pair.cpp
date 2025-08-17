#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
using namespace std;

class Solution{
public:
    struct coordinates{
        double x;
        double y;
    };

    void ClosestPair(coordinates* arr, int length){
        if (length < 2) {
            cout << "Array needs at least two points!\n";
            return;
        }

        double closest_x1 = 0.0, closest_y1 = 0.0;
        double closest_x2 = 0.0, closest_y2 = 0.0;
        double closest_distance = 1e9; 

        for (int i = 0; i < length - 1; ++i) {
            for (int j = i + 1; j < length; ++j) {
                coordinates ci = arr[i];
                coordinates cj = arr[j];

                double dx = cj.x - ci.x;
                double dy = cj.y - ci.y;
                double distance = sqrt(dx*dx + dy*dy);

                if (distance < closest_distance) {
                    closest_distance = distance;
                    closest_x1 = ci.x; closest_y1 = ci.y;
                    closest_x2 = cj.x; closest_y2 = cj.y;
                }
            }
        }

        cout << "Closest pair: ("
             << closest_x1 << ", " << closest_y1 << ") and ("
             << closest_x2 << ", " << closest_y2 << ")\n";
        cout << "The closest distance is: " << closest_distance << "\n";
    }
};

bool leerArchivo(const string& filename, Solution::coordinates*& arr, int& length) {
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "No se pudo abrir el archivo: " << filename << "\n";
        arr = nullptr;
        length = 0;
        return false;
    }

    length = 0;
    double x, y;
    while (file >> x >> y) {
        length++;
    }

    if (length == 0) {
        cerr << "Archivo vacio: " << filename << "\n";
        arr = nullptr;
        return false;
    }

    arr = new Solution::coordinates[length];
    file.clear();
    file.seekg(0, ios::beg);

    int i = 0;
    while (file >> x >> y) {
        arr[i].x = x;
        arr[i].y = y;
        i++;
    }
    file.close();
    return true;
}

int main() {
    Solution sol;

    Solution::coordinates* arr_n10 = nullptr;
    int len_n10 = 0;
    if (leerArchivo("fuerza_bruta/test_cases/closest_distance/puntos-n10.txt", arr_n10, len_n10)) {
        sol.ClosestPair(arr_n10, len_n10);
        delete[] arr_n10;
        cout << "---------------------------------\n";
    }

    Solution::coordinates* arr_n11 = nullptr;
    int len_n11 = 0;
    if (leerArchivo("fuerza_bruta/test_cases/closest_distance/puntos-n11.txt", arr_n11, len_n11)) {
        sol.ClosestPair(arr_n11, len_n11);
        delete[] arr_n11;
        cout << "---------------------------------\n";
    }

    Solution::coordinates* arr_n15 = nullptr;
    int len_n15 = 0;
    if (leerArchivo("fuerza_bruta/test_cases/closest_distance/puntos-n15.txt", arr_n15, len_n15)) {
        sol.ClosestPair(arr_n15, len_n15);
        delete[] arr_n15;
        cout << "---------------------------------\n";
    }

    Solution::coordinates* arr_n20 = nullptr;
    int len_n20 = 0;
    if (leerArchivo("fuerza_bruta/test_cases/closest_distance/puntos-n20.txt", arr_n20, len_n20)) {
        sol.ClosestPair(arr_n20, len_n20);
        delete[] arr_n20;
        cout << "---------------------------------\n";
    }

    Solution::coordinates* arr_n50 = nullptr;
    int len_n50 = 0;
    if (leerArchivo("fuerza_bruta/test_cases/closest_distance/puntos-n50.txt", arr_n50, len_n50)) {
        sol.ClosestPair(arr_n50, len_n50);
        delete[] arr_n50;
        cout << "---------------------------------\n";
    }

    Solution::coordinates* arr_n100 = nullptr;
    int len_n100 = 0;
    if (leerArchivo("fuerza_bruta/test_cases/closest_distance/puntos-n100.txt", arr_n100, len_n100)) {
        sol.ClosestPair(arr_n100, len_n100);
        delete[] arr_n100;
        cout << "---------------------------------\n";
    }

    return 0;
}
