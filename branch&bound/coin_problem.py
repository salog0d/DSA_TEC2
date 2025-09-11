"""
Branch-and-Bound para Coin-Collecting (movimientos: abajo / derecha)

Características:
- Lee instancias desde TXT en formatos: "R C" + matriz, "N" + matriz cuadrada, o matriz cruda.
- Usa una fila de prioridad (heapq) ordenada por cota superior (mayor primero).
- Imprime la ruta óptima como secuencia de (dirección, valor tomado en ese paso) y el Total.
- Incluye una heurística voraz para tener un incumbente inicial y podar agresivamente.

Ejecuta automáticamente sobre los casos típicos:
  coins-n5, coins-n7, coins-n8, coins-n9,
  coins-n10, coins-n12, coins-n20, coins-n100
"""

from heapq import heappush, heappop
from typing import List, Tuple
import re
import os

FILES = [
    "coins-n5 (1).txt",
    "coins-n7.txt",
    "coins-n8.txt",
    "coins-n9.txt",
    "coins-n10 (1).txt",
    "coins-n12.txt",
    "coins-n20 (1).txt",
    "coins-n100 (1).txt",
]

BASE_DIR = "branch&bound/instances/"   


def load_grid(path: str) -> List[List[int]]:
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    if not lines:
        raise ValueError("Archivo vacío")

    m_two = re.match(r"^\s*(\d+)\s+(\d+)\s*$", lines[0])
    if m_two:
        R, C = int(m_two.group(1)), int(m_two.group(2))
        rows = [list(map(int, ln.split())) for ln in lines[1:1+R]]
        if any(len(r) != C for r in rows) or len(rows) != R:
            raise ValueError("Dimensiones inconsistentes (R C).")
        return rows

    m_one = re.match(r"^\s*(\d+)\s*$", lines[0])
    if m_one:
        N = int(m_one.group(1))
        rows = [list(map(int, ln.split())) for ln in lines[1:1+N]]
        if any(len(r) != N for r in rows) or len(rows) != N:
            raise ValueError("Dimensiones inconsistentes (N).")
        return rows

    rows = [list(map(int, ln.split())) for ln in lines]
    C = len(rows[0])
    if any(len(r) != C for r in rows):
        raise ValueError("Matriz con filas de longitudes distintas.")
    return rows


def upper_bound(grid: List[List[int]], i: int, j: int, suma: int) -> int:
    """
    Cota admisible (optimista) desde (i,j) con acumulado 'suma'.
    Idea: de aquí al final hay exactamente 'pasos_restantes' movimientos,
    y por lo tanto se visitarán 'pasos_restantes' celdas adicionales.
    El mejor caso imposible (pero admisible como cota) sería tomar en
    cada paso el valor máximo M de la submatriz restante.
    UB = suma + pasos_restantes * M
    """
    R, C = len(grid), len(grid[0])
    if i == R - 1 and j == C - 1:
        return suma

    M = grid[i][j]
    for r in range(i, R):
        row = grid[r]
        for c in range(j, C):
            if row[c] > M:
                M = row[c]

    pasos_restantes = (R - 1 - i) + (C - 1 - j)  
    return suma + pasos_restantes * M


def greedy_initial(grid: List[List[int]]) -> Tuple[int, List[Tuple[str, int]]]:
    """
    Baja/derecha eligiendo localmente la mejor moneda inmediata.
    Devuelve (total, path) donde path es lista de (dirección, valor tomado).
    Nota: el 'total' incluye el valor de la celda inicial (0,0).
    """
    R, C = len(grid), len(grid[0])
    i, j = 0, 0
    total = grid[0][0]
    path: List[Tuple[str, int]] = []
    while not (i == R - 1 and j == C - 1):
        down_ok = (i + 1 < R)
        right_ok = (j + 1 < C)
        if down_ok and right_ok:
            if grid[i + 1][j] >= grid[i][j + 1]:
                i += 1
                val = grid[i][j]
                total += val
                path.append(("abajo", val))
            else:
                j += 1
                val = grid[i][j]
                total += val
                path.append(("derecha", val))
        elif down_ok:
            i += 1
            val = grid[i][j]
            total += val
            path.append(("abajo", val))
        else:
            j += 1
            val = grid[i][j]
            total += val
            path.append(("derecha", val))
    return total, path


def branch_and_bound(grid: List[List[int]]) -> Tuple[int, List[Tuple[str, int]]]:
    R, C = len(grid), len(grid[0])

    best_sum, best_path = greedy_initial(grid)

    start_sum = grid[0][0]
    root_ub = upper_bound(grid, 0, 0, start_sum)

    heap: List[Tuple[int, int, int, int, List[Tuple[str, int]]]] = []
    heappush(heap, (-root_ub, 0, 0, start_sum, []))

    while heap:
        neg_ub, i, j, suma, path = heappop(heap)
        ub = -neg_ub


        if ub <= best_sum:
            continue

        if i == R - 1 and j == C - 1:
            if suma > best_sum:
                best_sum = suma
                best_path = path
            continue

        if i + 1 < R:
            ni, nj = i + 1, j
            val = grid[ni][nj]
            suma2 = suma + val
            ub2 = upper_bound(grid, ni, nj, suma2)
            if ub2 > best_sum:  
                heappush(heap, (-ub2, ni, nj, suma2, path + [("abajo", val)]))

        if j + 1 < C:
            ni, nj = i, j + 1
            val = grid[ni][nj]
            suma2 = suma + val
            ub2 = upper_bound(grid, ni, nj, suma2)
            if ub2 > best_sum:
                heappush(heap, (-ub2, ni, nj, suma2, path + [("derecha", val)]))

    return best_sum, best_path


def print_solution(name: str, total: int, path: List[Tuple[str, int]]) -> None:
    seq = ", ".join(f"{d} ({v})" for d, v in path) if path else "(sin movimientos)"
    print(f"\n== {name} ==")
    print(f"{seq}. Total= {total}")

if __name__ == "__main__":
    for fname in FILES:
        fpath = os.path.join(BASE_DIR, fname)
        try:
            grid = load_grid(fpath)
            total, path = branch_and_bound(grid)
            print_solution(fname, total, path)
        except Exception as e:
            print(f"\n== {fname} ==")
            print("ERROR:", e)
