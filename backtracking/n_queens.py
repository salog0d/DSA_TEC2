# N-Queens iterativo por filas (todas las soluciones)
# ---------------------------------------------------
# ¿Qué hace?
#   Coloca n reinas en un tablero n x n sin que se ataquen (misma columna o diagonales),
#   explorando TODAS las soluciones con backtracking ITERATIVO (sin recursión), una fila a la vez.
#   Imprime cada solución en formato con "R" y "-" y, al final, la cantidad total de soluciones.
#   Si no existe ninguna (p. ej., n=2 o n=3), imprime que no se puede.
#
# Entrada:
#   Un entero n (n >= 1).
#
# Salida:
#   - Imprime cada solución hallada y un separador entre ellas.
#   - Al final, imprime "Total de soluciones para n={n}: {soluciones}".
#   - Si no hay soluciones, imprime "No se puede colocar {n} reinas en un tablero de {n}x{n}."
#
# Complejidad:
#   O(n)
    

def n_queens_iterativo(n: int) -> int:
    if n <= 0:
        print("n debe ser >= 1")
        return 0

    pos = [-1] * n
    col_usada = [False] * n
    d1_usada = [False] * (2 * n - 1)
    d2_usada = [False] * (2 * n - 1)

    fila = 0
    col_inicial = 0
    soluciones = 0

    def imprimir_solucion():
        if all(p != -1 for p in pos):
            for r in range(n):
                c = pos[r]
                fila_str = []
                for j in range(n):
                    fila_str.append("R" if j == c else "-")
                print("  ".join(fila_str))
                print()
            print("-" * (4 * n - 3))
        else:
            print("No se puede colocar todas las reinas en el tablero.\n")

    while fila >= 0:
        colocado = False
        for c in range(col_inicial, n):
            d1 = fila + c
            d2 = fila - c + (n - 1)
            if not col_usada[c] and not d1_usada[d1] and not d2_usada[d2]:
                pos[fila] = c
                col_usada[c] = True
                d1_usada[d1] = True
                d2_usada[d2] = True

                fila += 1
                col_inicial = 0
                colocado = True

                if fila == n:  
                    if all(p != -1 for p in pos):
                        soluciones += 1
                        imprimir_solucion()
                    else:
                        print("No se puede colocar todas las reinas en el tablero.\n")
                   
                    fila -= 1
                    c_prev = pos[fila]
                    col_usada[c_prev] = False
                    d1_usada[fila + c_prev] = False
                    d2_usada[fila - c_prev + (n - 1)] = False
                    col_inicial = c_prev + 1
                break
        if not colocado:
            if fila == 0:
                break
            fila -= 1
            c_prev = pos[fila]
            col_usada[c_prev] = False
            d1_usada[fila + c_prev] = False
            d2_usada[fila - c_prev + (n - 1)] = False
            col_inicial = c_prev + 1

    if soluciones == 0:
        print(f"No se puede colocar {n} reinas en un tablero de {n}x{n}.")
    else:
        print(f"Total de soluciones para n={n}: {soluciones}")
    return soluciones


if __name__ == "__main__":
    try:
        n = int(input("Ingresa n (>=1): ").strip())
    except Exception:
        n = 4
    n_queens_iterativo(n)
