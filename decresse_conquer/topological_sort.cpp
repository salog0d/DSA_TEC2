/*
Topological Sort (Kahn's Algorithm - BFS)

Description:
Encuentra un orden topológico en un grafo dirigido acíclico (DAG).
El algoritmo de Kahn usa indegree (grado de entrada) y una cola para
procesar nodos sin dependencias.

ALGORITHM topologicalSort(G)
Input: grafo dirigido representado como lista de adyacencia
Output: vector con un orden topológico válido

- Complejidad temporal: O(V + E), donde V = vértices, E = aristas
*/

#include <iostream>
#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    vector<int> topologicalSort(const vector<vector<int>>& G){
        int n = (int)G.size();
        vector<int> indeg(n, 0);

        for (int u = 0; u < n; ++u)
            for (int v : G[u])
                ++indeg[v];

        queue<int> q;
        for (int i = 0; i < n; ++i)
            if (indeg[i] == 0) q.push(i);

        vector<int> order;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            order.push_back(u);
            for (int v : G[u]) {
                if (--indeg[v] == 0) q.push(v);
            }
        }
        return order;
    }
};

int main() {
    Solution sol;
    vector<vector<int>> G = {
        {1,2},
        {3,},
        {3,4},
        {},
        {}
    };

    vector<int> n_order = sol.topologicalSort(G);
    for (int x : n_order) cout << x << " ";
    cout << "\n";
    return 0;
}
