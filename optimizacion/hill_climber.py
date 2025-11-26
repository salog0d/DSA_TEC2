import os
import random
import statistics
import matplotlib.pyplot as plt

def leer_grafo(path):
    edges = []
    with open(path, "r") as f:

        while True:
            line = f.readline()
            if not line:
                raise ValueError("No se encontró cabecera numérica")
            parts = line.strip().split()
            if parts and parts[0].isdigit():
                n = int(parts[0])
                break

        for line in f:
            line = line.strip()
            if not line:
                continue
            u, v = map(int, line.split())
            edges.append((u - 1, v - 1))  # 0-based
    return n, edges



def bandwidth(perm, edges):
    pos = [0] * len(perm)
    for i, v in enumerate(perm):
        pos[v] = i

    bw = 0
    for u, v in edges:
        d = abs(pos[u] - pos[v])
        if d > bw:
            bw = d
    return bw


def vecindario_first(S, edges, rng, evals, max_evals):
    n = len(S)
    O = list(range(n))
    rng.shuffle(O)

    costo_actual = bandwidth(S, edges)

    for i_idx in range(n):
        for j_idx in range(i_idx + 1, n):
            if evals >= max_evals:
                return S, evals

            i = O[i_idx]
            j = O[j_idx]

            V = S.copy()
            V[i], V[j] = V[j], V[i]

            c = bandwidth(V, edges)
            evals += 1

            if c < costo_actual:
                return V, evals

    return S, evals

def vecindario_best(S, edges, rng, evals, max_evals):
    n = len(S)
    O = list(range(n))
    rng.shuffle(O)

    costo_actual = bandwidth(S, edges)
    mejor_costo = costo_actual
    mejor_vecino = S

    for i_idx in range(n):
        for j_idx in range(i_idx + 1, n):
            if evals >= max_evals:
                return mejor_vecino, evals

            i = O[i_idx]
            j = O[j_idx]

            V = S.copy()
            V[i], V[j] = V[j], V[i]

            c = bandwidth(V, edges)
            evals += 1

            if c < mejor_costo:
                mejor_costo = c
                mejor_vecino = V

    return mejor_vecino, evals


def hill_climber(n, edges, max_evals, modo, rng):
    S = list(range(n))
    rng.shuffle(S)

    evals = 0
    mejor_perm = S
    mejor_costo = bandwidth(S, edges)

    while evals < max_evals:
        if modo == "first":
            V, evals = vecindario_first(S, edges, rng, evals, max_evals)
        elif modo == "best":
            V, evals = vecindario_best(S, edges, rng, evals, max_evals)
        else:
            raise ValueError("modo debe ser 'first' o 'best'")

        if V == S:
            break

        S = V
        c = bandwidth(S, edges)
        if c < mejor_costo:
            mejor_costo = c
            mejor_perm = S

    return mejor_costo, mejor_perm, evals


def correr_instancia(nombre, archivo, correr_first, correr_best, runs, max_evals):
    print(f"\n== Instancia {nombre} ({archivo}) ==")
    n, edges = leer_grafo(archivo)
    print(f"n = {n}, |E| = {len(edges)}")

    resultados = {"first": [], "best": []}

    if correr_first:
        print("  firstImprovement...")
        for r in range(runs):
            rng = random.Random(1000 + r)
            mejor_costo, _, _ = hill_climber(n, edges, max_evals, "first", rng)
            resultados["first"].append(mejor_costo)

    if correr_best:
        print("  bestImprovement...")
        for r in range(runs):
            rng = random.Random(2000 + r)
            mejor_costo, _, _ = hill_climber(n, edges, max_evals, "best", rng)
            resultados["best"].append(mejor_costo)

    # boxplot
    data = []
    labels = []
    if correr_first:
        data.append(resultados["first"])
        labels.append("firstImprovement")
    if correr_best:
        data.append(resultados["best"])
        labels.append("bestImprovement")

    if data:
        plt.figure()
        plt.boxplot(data)
        plt.xticks(range(1, len(labels) + 1), labels)
        plt.ylabel("Mejor bandwidth encontrado")
        plt.title(f"{nombre}: {runs} ejecuciones, {max_evals} evals/ejecución")
        plt.tight_layout()

        filename_plot = f"{nombre}_{'_'.join(labels)}.png"
        plt.savefig(filename_plot)
        plt.close()

        print(f"  Boxplot guardado en: {filename_plot}")


    for modo in ["first", "best"]:
        vals = resultados[modo]
        if not vals:
            continue
        print(
            f"  {modo:5s} -> "
            f"mean={statistics.mean(vals):.2f}, "
            f"median={statistics.median(vals):.2f}, "
            f"min={min(vals)}, max={max(vals)}"
        )

    return resultados


def menu():
    print("===================================")
    print(" Hill Climber - Bandwidth Problem ")
    print("===================================\n")

    instancias = {
        "1": ("bcspwr01", "bcspwr01 (1).txt"),
        "2": ("bcspwr02", "bcspwr02 (1).txt"),
        "3": ("bcspwr03", "bcspwr03 (1).txt"),
    }

    while True:
        print("Elige instancia:")
        print("  1) bcspwr01")
        print("  2) bcspwr02")
        print("  3) bcspwr03")
        print("  4) TODAS")
        print("  0) Salir")
        op_inst = input("Opción: ").strip()

        if op_inst == "0":
            print("Saliendo.")
            break
        if op_inst not in {"1", "2", "3", "4"}:
            print("Opción inválida.\n")
            continue

        print("\nTipo de improvement:")
        print("  1) firstImprovement (primer vecino que mejora)")
        print("  2) bestImprovement  (mejor de todos los vecinos)")
        print("  3) Ambos")
        op_modo = input("Opción: ").strip()
        if op_modo not in {"1", "2", "3"}:
            print("Opción inválida.\n")
            continue

        try:
            runs = int(input("Número de ejecuciones [50]: ") or "50")
            max_evals = int(input("Evaluaciones de vecinos por ejecución [250000]: ") or "250000")
        except ValueError:
            print("Número inválido.\n")
            continue

        correr_first = op_modo in {"1", "3"}
        correr_best = op_modo in {"2", "3"}

        if op_inst == "4":
            for key, (nombre, archivo) in instancias.items():
                if not os.path.exists(archivo):
                    print(f"Archivo {archivo} no encontrado, se omite.")
                    continue
                correr_instancia(nombre, archivo, correr_first, correr_best, runs, max_evals)
        else:
            nombre, archivo = instancias[op_inst]
            if not os.path.exists(archivo):
                print(f"Archivo {archivo} no encontrado.\n")
                continue
            correr_instancia(nombre, archivo, correr_first, correr_best, runs, max_evals)

        print("\n--- Terminado ---\n")

if __name__ == "__main__":
    menu()
