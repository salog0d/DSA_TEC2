from collections import deque

class Solution:
    
    @staticmethod
    def lee_grafo(archivo):
        with open(archivo, "r") as f:
            lines = f.read().strip().split("\n")
        n = int(lines[0].strip())
        matriz = [[0]*n for _ in range(n)]
        for line in lines[1:]:
            if not line.strip():
                continue
            u, v, capacidad = map(int, line.split())
            matriz[u][v] = capacidad
        return n, matriz

    @staticmethod
    def bfs_path(matriz, origen, destino):
        """
        Complejidad: O(n2)
        BFS que encuentra un camino entre origen y destino.
        Devuelve (camino, pesos)
        """
        n = len(matriz)
        visitado = [False]*n
        predecesor = [-1]*n
        cola = deque([origen])
        visitado[origen] = True

        # BFS estándar
        while cola:
            u = cola.popleft()
            for v in range(n):
                if matriz[u][v] > 0 and not visitado[v]:
                    visitado[v] = True
                    predecesor[v] = u
                    cola.append(v)
                    if v == destino:
                        cola.clear()
                        break

        # reconstrucción
        if not visitado[destino]:
            return [], []

        camino = []
        pesos = []
        nodo = destino
        while nodo != -1:
            camino.append(nodo)
            prev = predecesor[nodo]
            if prev != -1:
                pesos.append(matriz[prev][nodo])
            nodo = prev

        camino.reverse()
        pesos.reverse()
        return camino, pesos


def main():
    archivos = [
        "grafos/instances/flow-grafo.txt",
        "grafos/instances/flow-grafo-2.txt",
        "grafos/instances/flow-grafo-3.txt",
        "grafos/instances/flow-grafo-4.txt",
        "grafos/instances/flow-grafo-5.txt",
    ]

    for archivo in archivos:
        n, matriz = Solution.lee_grafo(archivo)
        origen, destino = 0, n - 1
        camino, pesos = Solution.bfs_path(matriz, origen, destino)
        print(camino)
        print(pesos)
        print("-"*30)


if __name__ == "__main__":
    main()
