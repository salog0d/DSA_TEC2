"""
Metaheurísticas simples para MinLA
ILS, Simulated Annealing, Hillclimber First/Best Improvement
Código limpio sin type-hints, sin clases.

-----------------------------------------------------------
Pseudocódigo usado
-----------------------------------------------------------

HILLCLIMBER FIRST-IMPROVEMENT
-----------------------------
S = permutación aleatoria
costS = cost(S)
evals = 0
mientras evals < MAX:
    mejoro = falso
    para i en orden aleatorio:
        para j > i en orden aleatorio:
            V = swap(S,i,j)
            evals++
            si cost(V) < costS:
                S = V
                costS = cost(V)
                mejoro = verdadero
                romper ambos ciclos
    si !mejoro: romper
regresar S

HILLCLIMBER BEST-IMPROVEMENT
----------------------------
S = perm inicial
costS = cost(S)
mientras true:
    best = S
    best_cost = costS
    para todos los i<j:
        evals++
        V = swap
        si cost(V) < best_cost:
            best = V
            best_cost = cost(V)
    si best_cost < costS:
        S = best
        costS = best_cost
    sino:
        romper

ILS
---
S = perm aleatoria
best = S
mientras evals < MAX:
    S_local = hillclimber_best(S)
    si cost(S_local) < cost(best):
        best = S_local
    S = perturbar(S_local,k_swaps)
regresar best

SIMULATED ANNEALING
-------------------
S = perm aleatoria
best = S
T = T0
mientras evals < MAX:
    V = swap aleatorio
    evals++
    delta = cost(V)-cost(S)
    si delta <=0: aceptar
    sino aceptar con prob exp(-delta/T)
    si cost(S) < cost(best): best=S
    cada n pasos: T = T * alpha
-----------------------------------------------------------
"""

import random
import math
import numpy as np
import matplotlib.pyplot as plt


# ==========================================================
# CARGA DEL GRAFO Y COSTO
# ==========================================================

def load_graph(path):
    with open(path, "r") as f:
        f.readline()       # nombre instancia
        header = f.readline().split()
        n = int(header[0])
        edges = []
        for line in f:
            line = line.strip()
            if line:
                u,v = map(int, line.split())
                edges.append((u,v))
    return n, edges


def cost_minla(perm, edges):
    pos = {perm[i]: i for i in range(len(perm))}
    total = 0
    for u,v in edges:
        total += abs(pos[u] - pos[v])
    return total


def random_perm(n, rng):
    perm = list(range(1, n+1))
    rng.shuffle(perm)
    return perm


def two_swap(perm, i, j):
    new = perm[:]
    new[i], new[j] = new[j], new[i]
    return new


# ==========================================================
# HILLCLIMBER FIRST IMPROVEMENT
# ==========================================================

def hc_first(perm_init, edges, max_evals, rng):
    n = len(perm_init)
    S = perm_init[:]
    costS = cost_minla(S, edges)
    evals = 0

    improved = True
    while improved and evals < max_evals:
        improved = False
        idx = list(range(n))
        rng.shuffle(idx)

        for a in range(n-1):
            i = idx[a]
            for b in range(a+1, n):
                j = idx[b]

                V = two_swap(S, i, j)
                evals += 1
                c = cost_minla(V, edges)

                if c < costS:
                    S = V
                    costS = c
                    improved = True
                    break
                if evals >= max_evals:
                    break
            if improved or evals >= max_evals:
                break

    return S, costS, evals


# ==========================================================
# HILLCLIMBER BEST IMPROVEMENT
# ==========================================================

def hc_best(perm_init, edges, max_evals, rng):
    n = len(perm_init)
    S = perm_init[:]
    costS = cost_minla(S, edges)
    evals = 0

    while evals < max_evals:
        best = S
        best_cost = costS
        idx = list(range(n))
        rng.shuffle(idx)

        for a in range(n-1):
            i = idx[a]
            for b in range(a+1, n):
                j = idx[b]
                V = two_swap(S, i, j)
                evals += 1
                c = cost_minla(V, edges)
                if c < best_cost:
                    best = V
                    best_cost = c
                if evals >= max_evals:
                    break
            if evals >= max_evals:
                break

        if best_cost < costS:
            S = best
            costS = best_cost
        else:
            break

    return S, costS, evals


# ==========================================================
# ILS
# ==========================================================

def perturb_k_swaps(perm, k, rng):
    n = len(perm)
    new = perm[:]
    for _ in range(k):
        i,j = rng.sample(range(n),2)
        new[i], new[j] = new[j], new[i]
    return new


def ils(perm_init, edges, max_evals, rng, k=4):
    S = perm_init[:]
    best = S
    best_cost = cost_minla(best, edges)
    evals = 0

    while evals < max_evals:
        remain = max_evals - evals
        S_local, c_local, used = hc_best(S, edges, remain, rng)
        evals += used

        if c_local < best_cost:
            best = S_local
            best_cost = c_local

        if evals >= max_evals:
            break

        S = perturb_k_swaps(S_local, k, rng)

    return best, best_cost, evals


# ==========================================================
# SIMULATED ANNEALING
# ==========================================================

def sa(perm_init, edges, max_evals, rng, T0=100, alpha=0.995, Tmin=1e-3):
    S = perm_init[:]
    costS = cost_minla(S, edges)
    best = S
    best_cost = costS

    evals = 0
    n = len(S)
    T = T0
    steps = 0

    while evals < max_evals:
        i,j = rng.sample(range(n),2)
        V = two_swap(S,i,j)

        evals += 1
        c = cost_minla(V, edges)
        delta = c - costS

        if delta <= 0:
            S = V
            costS = c
        else:
            if rng.random() < math.exp(-delta / max(T,1e-9)):
                S = V
                costS = c

        if costS < best_cost:
            best = S
            best_cost = costS

        steps += 1
        if steps % n == 0:
            T = max(T*alpha, Tmin)

    return best, best_cost, evals


# ==========================================================
# EXPERIMENTOS Y BOXPLOTS
# ==========================================================

def run_experiments():
    RUNS = 50
    MAX_EVALS = 250000
    base_seed = 12345

    instances = {
        "ash85": "last/ash85.txt",
        "bcspwr03": "last/bcspwr01.txt",
        "bcspwr03": "last/bcspwr02.txt",
        "bcspwr03": "last/bcspwr03.txt"
    }

    results = {inst:{} for inst in instances}

    for inst, path in instances.items():
        n, edges = load_graph(path)
        print("\nInstancia:", inst, "n=", n, "|E|=", len(edges))

        algos = {
            "HC_first": hc_first,
            "HC_best": hc_best,
            "ILS": ils,
            "SA": sa
        }

        for name, fn in algos.items():
            print("\n Algoritmo:", name)
            vals = []

            for run in range(RUNS):
                seed = base_seed + run*1000 + hash((inst,name))%999
                rng = random.Random(seed)
                perm0 = random_perm(n, rng)

                best, c, used = fn(perm0, edges, MAX_EVALS, rng)
                vals.append(c)
                print("   Run", run+1, "costo =", c)

            results[inst][name] = vals

    summarize(results, RUNS, MAX_EVALS)


def summarize(results, RUNS, MAX_EVALS):
    print("\n====================================")
    print("   RESUMEN NUMÉRICO")
    print("====================================")

    for inst, algos in results.items():
        print("\nInstancia:", inst)
        for name, vals in algos.items():
            arr = np.array(vals)
            print(" ", name.ljust(10),
                  "best=", int(arr.min()),
                  "mean=", round(arr.mean(),2),
                  "std=", round(arr.std(),2))

        # Boxplot
        labels = sorted(algos.keys())
        data = [algos[l] for l in labels]

        plt.figure()
        plt.boxplot(data, labels=labels, showmeans=True)
        plt.title(f"{inst} - {RUNS} corridas, {MAX_EVALS} evaluaciones")
        plt.xlabel("Algoritmo")
        plt.ylabel("Costo MinLA")
        plt.tight_layout()
        plt.savefig(f"boxplot_{inst}.png", dpi=200)
        plt.close()
        print(" Boxplot guardado:", f"boxplot_{inst}.png")


if __name__ == "__main__":
    run_experiments()
