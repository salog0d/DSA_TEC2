/*
Fuerza bruta: Tecnica para resolucion de algoritmos que computa todas las posibilidades de solucion de dicho algoritmo,
-No muy eficiente en la mayoria de los casos (busqueda secuencial, selection sort y bubble sort).

Closest Pair:

sqrt((y2 - y1)^2 + (x2 - x1)^2)

String matching:
*/
#include <iostream>
#include <cmath>
using namespace std;

class Solutions{
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
        double closest_distance = 1e9; // valor muy grande

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

int main() {
    Solutions sol;

    Solutions::coordinates arr[] = {
        { -2.423, -8.469 },
        {  5.721,  9.354 },
        {  6.766, -3.823 },
        {  4.129,  6.744 },
        {  5.371, -5.404 }
    };
    int length = sizeof(arr) / sizeof(arr[0]);

    sol.ClosestPair(arr, length);
    return 0;
}
