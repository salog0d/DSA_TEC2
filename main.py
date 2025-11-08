# -*- coding: utf-8 -*-
# ==============================================================================
# LIBRERÍAS NECESARIAS
# ==============================================================================
import math
import matplotlib.pyplot as plt


# ==============================================================================
# LECTURA DE PUNTOS DESDE ARCHIVO
# ==============================================================================
def lee_archivo(archivo):
    f = open(archivo, "r")
    contenido = f.read()
    f.close()

    lines = contenido.split("\n")
    n = int(lines[0])
    aux = [list(map(float, lines[i].split("\t"))) for i in range(1, len(lines)-1)]

    points = []
    for a in aux:
        points.append(Punto(a[0], a[1]))

    return n, points


# ==============================================================================
# PROBLEMA 1: UN TRIÁNGULO Y PUNTOS
# Clases para representar Puntos, Segmentos y Triángulos
# ==============================================================================
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        return [self.x, self.y]

    def __eq__(self, other):
        return isinstance(other, Punto) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f})"


class Segmento:
    def __init__(self, A, B):
        self.A = A
        self.B = B

    def show(self):
        return [self.A.x, self.A.y, self.B.x, self.B.y]

    def __eq__(self, other):
        return (
            isinstance(other, Segmento) and
            ((self.A == other.A and self.B == other.B) or (self.A == other.B and self.B == other.A))
        )

    def __hash__(self):
        # hash indiferente al orden de los extremos
        return hash(frozenset([hash(self.A), hash(self.B)]))

    def __str__(self):
        return f"[{self.A} -> {self.B}]"


class Triangulo:
    def __init__(self, puntos):
        self.puntos = puntos
        s1 = Segmento(puntos[0], puntos[1])
        s2 = Segmento(puntos[1], puntos[2])
        s3 = Segmento(puntos[2], puntos[0])
        self.lados = [s1, s2, s3]

        # PROBLEMA 2: Calcular centro y radio del círculo circunscrito
        self.centro, self.radio = self.calcular_circuncentro()

    # ==============================================================================
    # PROBLEMA 2: LA CIRCUNFERENCIA CIRCUNSCRITA
    # Cálculo del circuncentro y radio del círculo circunscrito al triángulo
    # ==============================================================================
    def calcular_circuncentro(self):
        """Calcula el centro y radio del círculo circunscrito"""
        p1, p2, p3 = self.puntos[0], self.puntos[1], self.puntos[2]

        ax, ay = p1.x, p1.y
        bx, by = p2.x, p2.y
        cx, cy = p3.x, p3.y

        D = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))

        if abs(D) < 1e-10:  # Puntos colineales
            return None, None

        ux = ((ax*ax + ay*ay) * (by - cy) +
              (bx*bx + by*by) * (cy - ay) +
              (cx*cx + cy*cy) * (ay - by)) / D
        uy = ((ax*ax + ay*ay) * (cx - bx) +
              (bx*bx + by*by) * (ax - cx) +
              (cx*cx + cy*cy) * (bx - ax)) / D

        centro = Punto(ux, uy)
        radio = math.sqrt((ax - ux)**2 + (ay - uy)**2)

        return centro, radio

    # ==============================================================================
    # PROBLEMA 3: PUNTOS DENTRO DE CÍRCULOS
    # Determina si un punto está dentro del círculo circunscrito
    # ==============================================================================
    def punto_en_circuncentro(self, punto):
        """Verifica si un punto está dentro del círculo circunscrito"""
        if self.centro is None or self.radio is None:
            return False

        distancia = math.sqrt((punto.x - self.centro.x)**2 + (punto.y - self.centro.y)**2)
        return distancia < self.radio

    def tiene_vertice(self, punto):
        """Verifica si el triángulo tiene el punto como vértice"""
        return punto in self.puntos

    def __str__(self):
        return f"Triángulo: {self.lados[0]}, {self.lados[1]}, {self.lados[2]}"


# ==============================================================================
# PROBLEMA 6: TRIANGULACIÓN DE DELAUNAY
# Implementación del Algoritmo Bowyer-Watson
# ==============================================================================
def crear_super_triangulo(puntos):
    """Crea un triángulo grande que contiene todos los puntos"""
    min_x = min(p.x for p in puntos)
    max_x = max(p.x for p in puntos)
    min_y = min(p.y for p in puntos)
    max_y = max(p.y for p in puntos)

    dx = max_x - min_x
    dy = max_y - min_y
    delta_max = max(dx, dy)
    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2

    p1 = Punto(mid_x - 20 * delta_max, mid_y - delta_max)
    p2 = Punto(mid_x, mid_y + 20 * delta_max)
    p3 = Punto(mid_x + 20 * delta_max, mid_y - delta_max)

    return Triangulo([p1, p2, p3])


# ==============================================================================
# PROBLEMA 5: GRÁFICAS
# Funciones para visualizar la triangulación en diferentes etapas
# ==============================================================================
def visualizar_paso(puntos, triangulos, titulo, mostrar_circulos=False, punto_actual=None):
    """Visualiza un paso de la triangulación"""
    plt.figure(figsize=(10, 10))

    # Dibujar triángulos
    for tri in triangulos:
        for lado in tri.lados:
            plt.plot([lado.A.x, lado.B.x], [lado.A.y, lado.B.y], 'b-', linewidth=0.5)

    # Dibujar círculos si se solicita
    if mostrar_circulos:
        for tri in triangulos:
            if tri.centro is not None and tri.radio is not None:
                circle = plt.Circle((tri.centro.x, tri.centro.y), tri.radio,
                                    fill=False, linestyle='--', linewidth=0.5, alpha=0.5)
                plt.gca().add_patch(circle)

    # Dibujar puntos
    xs = [p.x for p in puntos]
    ys = [p.y for p in puntos]
    plt.plot(xs, ys, 'ro', markersize=5)

    # Resaltar punto actual si existe
    if punto_actual is not None:
        plt.plot(punto_actual.x, punto_actual.y, 'go', markersize=10, label='Punto actual')
        plt.legend()

    plt.axis('equal')
    plt.title(titulo)
    plt.grid(True, alpha=0.3)
    plt.savefig(titulo.replace(' ', '_').replace(':', '') + '.png', dpi=150, bbox_inches='tight')
    plt.show()


# ==========================
# Utilidades de aristas (reemplazo de PROBLEMA 4)
# ==========================
def _edge_key_from_segment(seg: Segmento):
    """Llave invariante para una arista, independiente del orden de sus extremos."""
    p1 = (seg.A.x, seg.A.y)
    p2 = (seg.B.x, seg.B.y)
    return tuple(sorted([p1, p2]))


def _build_edge_maps(triangles):
    """
    Construye:
      - counts: dict[edge_key] -> cuántas veces aparece el edge en 'triangles'
      - rep:    dict[edge_key] -> un Segmento representativo (objeto original)
    """
    counts = {}
    rep = {}
    for tri in triangles:
        for lado in tri.lados:
            key = _edge_key_from_segment(lado)
            counts[key] = counts.get(key, 0) + 1
            if key not in rep:
                rep[key] = lado
    return counts, rep


def bowyer_watson(puntos, visualizar_pasos=True):
    """Implementa el algoritmo Bowyer-Watson para triangulación de Delaunay"""
    # Crear super triángulo
    bigTriangle = crear_super_triangulo(puntos)
    T = [bigTriangle]

    # Visualizar triángulo inicial
    if visualizar_pasos:
        visualizar_paso(puntos, T, "Paso 0: Triángulo inicial", mostrar_circulos=True)

    # Para cada punto
    for idx, p in enumerate(puntos):
        badTriangles = []

        # PROBLEMA 3: Encontrar triángulos cuyo círculo contiene a p
        for triangulo in list(T):
            if triangulo.punto_en_circuncentro(p):
                badTriangles.append(triangulo)

        # ==================================================================
        # PROBLEMA 4: LADOS NO COMPARTIDOS (versión con mapa de aristas)
        # Encontrar lados únicos (no compartidos entre badTriangles)
        # ==================================================================
        counts, rep = _build_edge_maps(badTriangles)
        unicos = [rep[key] for key, c in counts.items() if c == 1]

        # Remover bad triangles
        for tri in badTriangles:
            if tri in T:
                T.remove(tri)

        # Crear nuevos triángulos
        for lado in unicos:
            nuevoTri = Triangulo([p, lado.A, lado.B])
            T.append(nuevoTri)

        # Visualizar estado después de agregar este punto
        if visualizar_pasos:
            visualizar_paso(puntos[:idx+1], T,
                            f"Paso {idx+1}: Después de agregar punto {idx+1} {p}",
                            mostrar_circulos=True, punto_actual=p)

    # Remover triángulos que comparten vértices con el super triángulo
    vertices_super = bigTriangle.puntos
    T_final = []
    for tri in T:
        tiene_vertice_super = False
        for v in vertices_super:
            if tri.tiene_vertice(v):
                tiene_vertice_super = True
                break

        if not tiene_vertice_super:
            T_final.append(tri)

    return T_final


def imprimir_triangulos(triangulos):
    """Imprime la lista de triángulos con formato"""
    print("\n" + "="*80)
    print("LISTADO DE TRIÁNGULOS DE LA TRIANGULACIÓN DE DELAUNAY")
    print("="*80)

    for idx, tri in enumerate(triangulos, 1):
        print(f"\nTriángulo {idx}:")
        for i, lado in enumerate(tri.lados, 1):
            print(f"  Segmento {i}: {lado}")

    print("\n" + "="*80)


# ==============================================================================
# PROGRAMA PRINCIPAL - EJECUCIÓN
# ==============================================================================
if __name__ == "__main__":
    # Ejecutar el algoritmo
    print("Iniciando Triangulación de Delaunay - Algoritmo Bowyer-Watson")
    print("="*80)

    n, points = lee_archivo('puntos-n10.txt')
    print(f"\nNúmero de puntos leídos: {n}")
    print(f"Puntos: {[str(p) for p in points]}")

    print("\nGenerando triangulación con visualización de pasos intermedios...")
    triangulos = bowyer_watson(points, visualizar_pasos=True)

    print(f"\nNúmero de triángulos generados: {len(triangulos)}")

    # Imprimir lista de triángulos
    imprimir_triangulos(triangulos)

    # Visualizar resultado final SIN círculos
    print("\nGenerando gráfica final sin círculos...")
    visualizar_paso(points, triangulos,
                    "Resultado Final: Triangulación de Delaunay (sin círculos)",
                    mostrar_circulos=False)

    # Visualizar resultado final CON círculos
    print("Generando gráfica final con círculos...")
    visualizar_paso(points, triangulos,
                    "Resultado Final: Triangulación de Delaunay (con círculos)",
                    mostrar_circulos=True)

    print("\n¡Proceso completado!")
    print("Se han generado las siguientes gráficas:")
    print("- Triángulo inicial con su círculo")
    print(f"- {n} gráficas de pasos intermedios (una por cada punto agregado)")
    print("- 2 gráficas finales (con y sin círculos circunscritos)")
