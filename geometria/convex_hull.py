#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convex Hull con QuickHull (SIN PDF)
- Lee TODOS los .txt/.tsv/.dat en 'instances/' (formato: primera línea N, luego N líneas "x y" o "x\t y")
- Para cada archivo genera: <base>_hull_points.txt y <base>_hull.png en 'outputs/'

Uso:
  python convex_hull_quickhull.py --input_dir instances --output_dir outputs
"""

import math
import argparse
from pathlib import Path
from typing import List, Tuple
import matplotlib.pyplot as plt


# ------------------------------- I/O helpers -------------------------------

def read_points_file(path: str) -> List[Tuple[float, float]]:
    """Lee archivo: primera línea N, luego N líneas con x y (espacio o tab)."""
    points: List[Tuple[float, float]] = []
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]
    if not lines:
        return points
    try:
        n = int(lines[0])
        coord_lines = lines[1:1+n]
    except ValueError:
        coord_lines = lines
    for ln in coord_lines:
        parts = ln.replace("\t", " ").split()
        if len(parts) >= 2:
            try:
                x, y = float(parts[0]), float(parts[1])
                points.append((x, y))
            except ValueError:
                continue
    return points


def write_hull_points(path: str, hull: List[Tuple[float, float]]):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{len(hull)}\n")
        for x, y in hull:
            f.write(f"{x}\t{y}\n")


# ----------------------------- Geometry helpers ----------------------------

def cross(o: Tuple[float, float], a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Producto cruz entre OA y OB (positivo si giro CCW)."""
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])


def point_line_distance(a: Tuple[float, float], b: Tuple[float, float], p: Tuple[float, float]) -> float:
    """Distancia perpendicular de p a la recta AB."""
    area2 = abs(cross(a, b, p))
    base = math.hypot(b[0]-a[0], b[1]-a[1])
    return area2 / base if base != 0 else 0.0


# -------------------------- QuickHull (NO Graham) --------------------------

def quickhull(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """Devuelve los vértices del casco convexo en orden CCW."""
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts

    a = min(pts, key=lambda p: (p[0], p[1]))  # min x
    b = max(pts, key=lambda p: (p[0], p[1]))  # max x

    left  = [p for p in pts if cross(a, b, p) > 0]
    right = [p for p in pts if cross(a, b, p) < 0]

    hull: List[Tuple[float, float]] = []

    def add_hull(p1: Tuple[float, float], p2: Tuple[float, float], S: List[Tuple[float, float]]):
        if not S:
            hull.append(p1)
            return
        far = max(S, key=lambda p: point_line_distance(p1, p2, p))
        s1 = [p for p in S if cross(p1, far, p) > 0]
        s2 = [p for p in S if cross(far, p2, p) > 0]
        add_hull(p1, far, s1)
        add_hull(far, p2, s2)

    add_hull(a, b, left)
    add_hull(b, a, right)
    hull.append(b)

    ordered, seen = [], set()
    for p in hull:
        if p not in seen:
            ordered.append(p)
            seen.add(p)
    return ordered


# -------------------------------- Plotting ---------------------------------

def plot_points_and_hull(points: List[Tuple[float, float]], hull: List[Tuple[float, float]],
                         title: str, save_path: str):
    """Grafica puntos + polígono del casco (cerrado)."""
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6, 6))
    if points:
        xs, ys = zip(*points)
        plt.scatter(xs, ys, s=20)  # sin fijar colores/estilos
    if hull and len(hull) >= 2:
        poly = hull + [hull[0]]
        hx, hy = zip(*poly)
        plt.plot(hx, hy, linewidth=2)
    plt.title(title)
    plt.xlabel("x"); plt.ylabel("y")
    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()


# --------------------------------- Main ------------------------------------

def main():
    # Versión simple: usa carpetas por defecto y sin argparse.
    in_dir  = Path("geometria/instances")
    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Toma todos los .txt/.tsv/.dat
    exts = (".txt", ".tsv", ".dat")
    files = sorted(p for ext in exts for p in in_dir.glob(f"*{ext}"))
    if not files:
        print(f"[Aviso] No hay archivos en {in_dir.resolve()}")
        return

    for f in files:
        pts  = read_points_file(str(f))
        hull = quickhull(pts)
        base = f.stem

        plot_points_and_hull(pts, hull, f"Convex Hull — {base}", str(out_dir / f"{base}_hull.png"))
        write_hull_points(str(out_dir / f"{base}_hull_points.txt"), hull)

        print(f"[OK] {base}: {len(hull)} vértices")
        
if __name__ == "__main__":
    main()

