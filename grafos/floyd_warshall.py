from copy import deepcopy
from math import inf

def warshall(A):
    """Calcula la clausura transitiva de una matriz de adyacencia (0/1)."""
    n = len(A)
    T = deepcopy(A)
    for k in range(n):
        for i in range(n):
            if T[i][k]:
                for j in range(n):
                    T[i][j] = 1 if (T[i][j] or (T[i][k] and T[k][j])) else 0
    return T
# Complejidad: O(n³)

def floyd(B):
    """Calcula las distancias más cortas entre todos los nodos (Floyd–Warshall)."""
    n = len(B)
    L = deepcopy(B)
    R = [[None]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j and L[i][j] != inf:
                R[i][j] = i

    for k in range(n):
        for i in range(n):
            dik = L[i][k]
            if dik == inf:
                continue
            for j in range(n):
                alt = dik + L[k][j]
                if alt < L[i][j]:
                    L[i][j] = alt
                    R[i][j] = R[k][j]
    return L, R
# Complejidad: O(n³)

def reconstruct_path(u, v, R):
    """Reconstruye el camino más corto entre dos nodos."""
    if u == v:
        return [u]
    if R[u][v] is None:
        return []
    path = [v]
    while v != u:
        v = R[u][v]
        if v is None:
            return []
        path.append(v)
    path.reverse()
    return path
# Complejidad: O(n)

A = [
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0],
    [1, 0, 1, 0],
]

x = float('inf')
B = [
    [0,   x, 3,   x],
    [2,   0, x,   x],
    [x,   6, 0,   1],
    [7,   x, x,   0],
]

n = 4
letras = ['a', 'b', 'c', 'd']

T = warshall(A)
print("Clausura transitiva (Warshall):")
for row in T:
    print(row)

L, R = floyd(B)
print("\nDistancias mínimas (Floyd–Warshall):")
for row in L:
    print(row)

u, v = 0, 3
path_idx = reconstruct_path(u, v, R)
path_labels = [letras[i] for i in path_idx] if path_idx else []
print(f"\nCamino más corto {letras[u]} -> {letras[v]}:", " -> ".join(path_labels) if path_labels else "sin camino")
print("Distancia:", L[u][v])
