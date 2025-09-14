#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Greedy para Coin-Collecting (grid con movimientos abajo/derecha y valores arbitrarios 1,2,5,...).

Estrategia greedy diseñada:
    - En cada celda (i,j) elegimos el siguiente movimiento entre {derecha, abajo}
      comparando un "potencial local":
          potential(move) = valor_del_vecino + suffix_max_del_subcuadrante_al_que_lleva
      donde suffix_max[a][b] es el valor máximo de cualquier celda en el subcuadrante
      alcanzable desde (a,b) (índice máximo en la submatriz a..n-1, b..m-1). Es un estimador
      optimista del "futuro" y nos ayuda a desempatar de forma informada.
    - Si solo uno de los movimientos es válido (borde), tomamos ese.
    - Registramos la ruta y el total de monedas recogidas.

¿Por qué es greedy?
    - La decisión en cada paso se toma con información local (vecinos inmediatos)
      y un estimador estático (suffix_max). No hay re-optimización global ni backtracking.

¿Dónde puede fallar (no óptimo)?
    - El estimador puede sobrevalorar una rama y perder combinaciones futuras
      que sumen más. Es un método aproximado.

Formato de entrada (archivo .txt):
    - Primera línea: n m   (filas y columnas)
    - Luego n líneas con m enteros separados por espacios (valores de monedas).
Salida (stdout):
    - Ruta (secuencia de movimientos) y valores recogidos por paso
    - Total acumulado
    - Comentarios de complejidad

Complejidad (peor caso):
    - Pre-cálculo de suffix_max: O(n*m)
    - Recorrido greedy de la ruta: O(n+m)
    - Total dominado por O(n*m)

Uso:
    python coin_collecting_greedy.py grid1.txt grid2.txt ...
"""


from typing import List, Tuple
import glob, sys, os, re

def _parse_dims(s: str) -> Tuple[int, int]:
    # normaliza separadores: x, X, *, ×, coma, punto y coma, tabs, etc
    norm = re.sub(r"[xX\*×,;]", " ", s.strip())
    parts = [p for p in norm.split() if p]
    nums = []
    for p in parts:
        # permite algo como "20#coment" -> extrae prefijo numérico
        m = re.match(r"^\d+", p)
        if m:
            nums.append(int(m.group(0)))
    if not nums:
        raise ValueError("No se encontraron números de dimensiones en la primera línea.")
    if len(nums) == 1:
        n = m = nums[0]
    else:
        n, m = nums[0], nums[1]
    return n, m

def parse_grid(path: str) -> List[List[int]]:
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
    n, m = _parse_dims(lines[0])

    grid: List[List[int]] = []
    for ln in lines[1:1+n]:
        # permite separadores variados también en las filas
        row_txt = re.sub(r"[,\t;]", " ", ln)
        row = [int(x) for x in row_txt.split()]
        if len(row) != m:
            raise ValueError(f"Fila con {len(row)} columnas, se esperaban {m} en {path}.")
        grid.append(row)
    if len(grid) != n:
        raise ValueError(f"Se declararon {n} filas pero se leyeron {len(grid)} en {path}.")
    return grid

def build_suffix_max(grid: List[List[int]]) -> List[List[int]]:
    n, m = len(grid), len(grid[0])
    sfx = [[0]*m for _ in range(n)]
    for i in range(n-1, -1, -1):
        for j in range(m-1, -1, -1):
            best = grid[i][j]
            if i+1 < n: best = max(best, sfx[i+1][j])
            if j+1 < m: best = max(best, sfx[i][j+1])
            if i+1 < n and j+1 < m: best = max(best, sfx[i+1][j+1])
            sfx[i][j] = best
    return sfx

def greedy_route(grid: List[List[int]]) -> Tuple[List[str], List[int], int]:
    n, m = len(grid), len(grid[0])
    sfx = build_suffix_max(grid)
    i = j = 0
    path_moves: List[str] = []
    picked_values: List[int] = [grid[0][0]]
    total = grid[0][0]

    while not (i == n-1 and j == m-1):
        candidates = []
        if j+1 < m:
            pot_right = grid[i][j+1] + sfx[i][j+1]
            candidates.append(("derecha", i, j+1, pot_right))
        if i+1 < n:
            pot_down = grid[i+1][j] + sfx[i+1][j]
            candidates.append(("abajo", i+1, j, pot_down))
        move, ni, nj, _ = max(candidates, key=lambda t: t[3])
        path_moves.append(move)
        i, j = ni, nj
        picked_values.append(grid[i][j])
        total += grid[i][j]

    return path_moves, picked_values, total

def describe(path_moves: List[str], picked: List[int], total: int) -> str:
    steps = []
    for mv, val in zip(["inicio"] + path_moves, picked):
        if mv == "inicio":
            steps.append(f"inicio ({val})")
        else:
            steps.append(f"{mv} ({val})")
    return ", ".join(steps) + f". Total = {total}"

def main():
    test_dir = os.path.join(os.getcwd(), "greedy", "test")
    if not os.path.isdir(test_dir):
        print(f"No existe la carpeta {test_dir}")
        sys.exit(1)

    # Solo archivos de coin-collecting
    files = sorted(glob.glob(os.path.join(test_dir, "coins*.txt")))
    if not files:
        print(f"No se encontraron archivos coins*.txt en {test_dir}")
        sys.exit(1)

    print("="*70)
    for p in files:
        print(f"Archivo: {p}")
        try:
            grid = parse_grid(p)
            moves, picked, total = greedy_route(grid)
            print(describe(moves, picked, total))
        except Exception as e:
            print(f"Error procesando {p}: {e}")
        print("-"*70)
    print("="*70)

if __name__ == "__main__":
    main()