#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Greedy heuristic for 0/1 Knapsack (ratio = value/weight).

Entrada (archivo .txt típico):
    - Primera línea: n C
        n = número de objetos
        C = capacidad entera del knapsack
    - Siguientes n líneas: w_i v_i  (peso y valor por objeto, separados por espacios)
      Se permiten líneas vacías o comentarios que empiecen con '#'.
Salida (stdout):
    - Lista de objetos elegidos (índices 0..n-1), su (peso, valor, ratio)
    - Peso total y valor total
    - Comentarios sobre complejidad, por qué es greedy y casos donde no da óptimo.

Complejidad (peor caso):
    - Ordenamiento por ratio: O(n log n)
    - Recorrido lineal para seleccionar: O(n)
    - Total: O(n log n)

¿Por qué es greedy?
    - Toma decisiones locales: siempre intenta elegir el siguiente objeto con mayor ratio valor/peso.
    - No re-considera decisiones previas (no hay backtracking).

¿Dónde puede fallar (no óptimo)?
    - En 0/1 Knapsack no es óptimo en general: un objeto muy pesado con ratio alto puede impedir tomar dos
      objetos de menor ratio que juntos den más valor. Es un método aproximado.

Uso:
    python knapsack_greedy.py instancia1.txt instancia2.txt ...
"""
from dataclasses import dataclass
from typing import List, Tuple
import sys, os, glob

@dataclass
class Item:
    idx: int
    w: int
    v: int
    ratio: float

def parse_knapsack_file(path: str) -> Tuple[int, List[Item]]:
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
    # primera linea: n C
    n_cap = lines[0].replace(",", " ").split()
    if len(n_cap) < 2:
        raise ValueError(f"Formato inválido en {path}: se espera 'n C' en la primera línea.")
    n, C = int(float(n_cap[0])), int(float(n_cap[1]))

    items: List[Item] = []
    for i, ln in enumerate(lines[1:1+n]):
        parts = ln.replace(",", " ").split()
        if len(parts) < 2:
            raise ValueError(f"Línea inválida en {path}: '{ln}'")
        w, v = int(float(parts[0])), int(float(parts[1]))
        ratio = (v / w) if w != 0 else float("inf")
        items.append(Item(idx=i, w=w, v=v, ratio=ratio))

    if len(items) != n:
        raise ValueError(f"Se declararon {n} objetos pero se leyeron {len(items)} en {path}.")
    return C, items

def greedy_knapsack(C: int, items: List[Item]):
    items_sorted = sorted(items, key=lambda x: x.ratio, reverse=True)
    picked = []
    total_w = 0
    total_v = 0
    for it in items_sorted:
        if total_w + it.w <= C:
            picked.append(it)
            total_w += it.w
            total_v += it.v
    return picked, total_w, total_v

def main():
    test_dir = os.path.join(os.getcwd(), "greedy", "test")
    if not os.path.isdir(test_dir):
        print(f"No existe la carpeta {test_dir}")
        sys.exit(1)

    files = sorted(glob.glob(os.path.join(test_dir, "*kp*.txt")))
    if not files:
        print(f"No se encontraron archivos *kp*.txt en {test_dir}")
        sys.exit(1)

    print("="*70)
    for p in files:
        print(f"Archivo: {p}")
        try:
            C, items = parse_knapsack_file(p)
            picked, tw, tv = greedy_knapsack(C, items)
            print(f"Capacidad: {C}")
            print("Objetos elegidos (idx, peso, valor, ratio):")
            for it in picked:
                print(f"  {it.idx:>3d}  (w={it.w}, v={it.v}, ratio={it.ratio:.4f})")
            print(f"Totales -> Peso: {tw}, Valor: {tv}")
        except Exception as e:
            print(f"Error procesando {p}: {e}")
        print("-"*70)
    print("="*70)

if __name__ == "__main__":
    main()