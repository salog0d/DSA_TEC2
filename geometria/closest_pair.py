import math
import os

class Solution:

    @staticmethod
    def read_file(path: str):
        points = []
        with open(path, "r") as f:
            lines = f.readlines()[1:]

        for line in lines:
            if not line.strip():
                continue
            x, y = map(float, line.split())
            points.append((x, y))

        return points

    @staticmethod
    def order_by_axis(S):
        OX = sorted(S, key=lambda p: p[0])
        OY = sorted(S, key=lambda p: p[1])
        return OX, OY
    
    @staticmethod
    def distance(S, S2):
        x1, y1 = S[0], S[1]
        x2, y2 = S2[0], S2[1]
        d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return d

    @staticmethod
    def findClosest3(points):
        if len(points) != 3:
            raise ValueError("Debe recibir exactamente 3 puntos.")

        p1, p2, p3 = points
        pairs = [
            ((p1, p2), Solution.distance(p1, p2)),
            ((p1, p3), Solution.distance(p1, p3)),
            ((p2, p3), Solution.distance(p2, p3)),
        ]
        return min(pairs, key=lambda x: x[1])
    
    @staticmethod
    def find_closest(OX, OY):
        """
        OX: lista de puntos ordenados por x
        OY: lista de puntos ordenados por y
        Retorna: (distancia_minima, (punto1, punto2))
        Complejidad: O(nlogn)
        """
        n = len(OX)
        if n == 2:
            d = Solution.distance(OX[0], OX[1])
            return d, (OX[0], OX[1])
        if n == 3:
            pair, d = Solution.findClosest3(OX)
            return d, pair

        mid = n // 2
        mid_x = OX[mid][0]

        # Partición izquierda/derecha 
        leftX = OX[:mid]
        rightX = OX[mid:]
        left_set = set(leftX) 

        OY_L = [p for p in OY if p in left_set]
        OY_R = [p for p in OY if p not in left_set]

        minL, closestL = Solution.find_closest(leftX, OY_L)
        minR, closestR = Solution.find_closest(rightX, OY_R)

        if minL < minR:
            minA, closestA = minL, closestL
        else:
            minA, closestA = minR, closestR

        S = [p for p in OY if abs(p[0] - mid_x) < minA]

        m = len(S)
        for i in range(m):
            for j in range(i + 1, min(i + 8, m)):
                d = Solution.distance(S[i], S[j])
                if d < minA:
                    minA = d
                    closestA = (S[i], S[j])

        return minA, closestA


def main():
    folder = "geometria/instances"
    files = sorted([f for f in os.listdir(folder) if f.endswith(".txt")])

    for filename in files:
        path = os.path.join(folder, filename)
        print(f"\nProcesando: {filename}")

        points = Solution.read_file(path)
        OX, OY = Solution.order_by_axis(points)

        min_dist, closest_pair = Solution.find_closest(OX, OY)

        print(f"  ➤ Puntos más cercanos: {closest_pair}")
        print(f"  ➤ Distancia mínima: {min_dist:.6f}")


if __name__ == "__main__":
    main()