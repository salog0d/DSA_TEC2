import re
import heapq
from datetime import datetime, timedelta

class Solution:

    # Formato esperado por línea:
    # (x1, y1) (x2, y2) d
    # Ej: (0,0) (0,1) 100
    LINE_RX = re.compile(
        r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*"     # (x1,y1)
        r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*"     # (x2,y2)
        r"(-?\d+(?:\.\d+)?)\s*$"                  # distancia (soporta float)
    )

    class Node:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.name = f"({x},{y})"
            self.connections = []  # nombres (solo informativo)

    @staticmethod
    def parse_line(line: str):
        """
        Parsea una línea del archivo y devuelve (x1, y1, x2, y2, d) o None si no matchea.
        """
        m = Solution.LINE_RX.match(line.strip())
        if not m:
            return None
        x1, y1, x2, y2, d = m.groups()
        # d puede ser float en el archivo
        return int(x1), int(y1), int(x2), int(y2), float(d)

    @staticmethod
    def generate_city(path: str):
        """
        Lee el archivo y genera:
        - adj: dict[(x,y)] -> list[( (nx,ny), dist )]
        - nodes: dict[(x,y)] -> Node (opcional/informativo)
        """
        adj: dict[tuple[int, int], list[tuple[tuple[int, int], float]]] = {}
        nodes: dict[tuple[int, int], Solution.Node] = {}

        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                raw = raw.strip()
                if not raw:
                    continue
                parsed = Solution.parse_line(raw)
                if not parsed:
                    # Línea inválida: ignorar (evita TypeError en unpack)
                    continue
                x1, y1, x2, y2, d = parsed
                a = (x1, y1)
                b = (x2, y2)

                if a not in nodes:
                    nodes[a] = Solution.Node(*a)
                if b not in nodes:
                    nodes[b] = Solution.Node(*b)

                # Conectar ambos lados (grafo no dirigido)
                nodes[a].connections.append(nodes[b].name)
                nodes[b].connections.append(nodes[a].name)

                adj.setdefault(a, []).append((b, d))
                adj.setdefault(b, []).append((a, d))

        return adj, nodes

    @staticmethod
    def dijkstra(adj: dict, start: tuple[int, int], goal: tuple[int, int]):
        """
        Dijkstra estándar:
        - adj: dict[(x,y)] -> list[( (nx,ny), dist )]
        Retorna:
        - dist_total (float)
        - path (list[(x,y)]) desde start hasta goal
        - edge_lengths (list[float]) longitudes por cuadra siguiendo path
        """
        INF = float("inf")
        dist = {start: 0.0}
        prev = {}
        pq = [(0.0, start)]

        while pq:
            cur_d, u = heapq.heappop(pq)
            if cur_d > dist.get(u, INF):
                continue
            if u == goal:
                break
            for v, w in adj.get(u, []):
                nd = cur_d + w
                if nd < dist.get(v, INF):
                    dist[v] = nd
                    prev[v] = (u, w)  # guarda también el peso de la arista
                    heapq.heappush(pq, (nd, v))

        if goal not in dist:
            return INF, [], []

        # Reconstruir ruta y longitudes por cuadra (de goal -> start)
        path_rev = []
        edge_lengths_rev = []
        cur = goal
        while cur != start:
            path_rev.append(cur)
            pu, w = prev[cur]
            edge_lengths_rev.append(w)
            cur = pu
        path_rev.append(start)

        path = list(reversed(path_rev))
        edge_lengths = list(reversed(edge_lengths_rev))

        return dist[goal], path, edge_lengths

    @staticmethod
    def calculate_time(velocity_m_per_min: float, distance_m: float) -> float:
        """
        Regresa minutos = distancia / velocidad
        """
        return distance_m / velocity_m_per_min

def main():
    # Configuración
    file = "grafos/city_2020.txt"
    damian = (2, 3)
    salida_hora = "17:00"  # todos salen a esta hora
    # Amigos: (nombre, (x,y), velocidad m/min)
    amigos = [
        ("Carlos",  (7, 4), 30),
        ("Ana",     (0, 19), 40),
        ("Marcela", (8, 12), 25),
        ("Katia",   (5, 17), 32),
        ("Marcos",  (17, 15), 20),
    ]

    # Cargar grafo
    adj, _nodes = Solution.generate_city(file)

    # Resolver por amigo
    resultados = []  # (nombre, dist_total, tiempo_min, path, edges)
    for nombre, start, vel in amigos:
        dist_total, ruta, long_cuadras = Solution.dijkstra(adj, start, damian)
        if dist_total == float("inf"):
            # No hay ruta
            print(f"{nombre}: no existe ruta hacia {damian}")
            continue
        tiempo_min = Solution.calculate_time(vel, dist_total)
        resultados.append((nombre, dist_total, tiempo_min, ruta, long_cuadras))

    # Imprimir resultados por amigo en el formato solicitado
    for nombre, dist_total, tiempo_min, ruta, long_cuadras in resultados:
        print(f"\n{nombre}:  {int(round(dist_total))} metros_totales   {tiempo_min:.2f} min")
        # Secuencia de posiciones
        print(", ".join(f"({x}, {y})" for x, y in ruta))
        # Longitud de cada cuadra
        if long_cuadras:
            print(", ".join(str(int(round(d))) for d in long_cuadras))
        else:
            print("")

    # Secuencia de llegada (si todos salen al mismo tiempo)
    # Ordenar por tiempo_min ascendente
    orden = sorted(resultados, key=lambda x: x[2])
    print("\nSecuencia de llegada: " + ", ".join(n for n, *_ in orden))

    # Calcular hora en que todos ya llegaron (max de tiempos)
    if orden:
        max_min = max(t for *_skip, t, _ruta, _edges in [(r[0], r[2], r[3], r[4]) for r in resultados])
        # Interpretar salida_hora como HH:MM del día actual (no se usa fecha real)
        base = datetime.strptime(salida_hora, "%H:%M")
        llegada_final = (base + timedelta(minutes=max_min)).strftime("%H:%M")
        print(f"Todos ya llegaron a las: {llegada_final}")

if __name__ == "__main__":
    main()
