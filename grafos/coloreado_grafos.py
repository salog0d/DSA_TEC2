from typing import Dict, List, Tuple, Optional

PALETTE: Dict[int, str] = {
    0: "morado",
    1: "amarillo",
    2: "azul",
    3: "verde",
    4: "naranja",
}


class Solution:
    @staticmethod
    def _smallest_available_color(u: str, G: Dict[str, List[str]], color: Dict[str, int]) -> int:
        used = {color[v] for v in G[u] if v in color}
        c = 0
        while c in used:
            c += 1
        return c

    @staticmethod
    def _with_names(color_idx: Dict[str, int]) -> Dict[str, Tuple[int, str]]:
        return {u: (c, PALETTE.get(c, f"color_{c}")) for u, c in color_idx.items()}

    @staticmethod
    def basic_greedy(G: Dict[str, List[str]], order: Optional[List[str]] = None):
        """Complejidad: tiempo O(n + m), espacio O(n), donde n=|V|, m=|E|."""
        if order is None:
            order = sorted(G.keys())

        color: Dict[str, int] = {}
        for u in order:
            color[u] = Solution._smallest_available_color(u, G, color)

        k = len(set(color.values()))
        return Solution._with_names(color), k

    @staticmethod
    def welsh_powell(G: Dict[str, List[str]]):
        """Complejidad: tiempo O(n^2 + m), espacio O(n)."""
        order = sorted(G.keys(), key=lambda u: len(G[u]), reverse=True)
        uncolored = set(order)
        color: Dict[str, int] = {}
        current = 0

        while uncolored:
            layer: List[str] = []
            for u in order:
                if u in uncolored and all(v not in G[u] for v in layer):
                    layer.append(u)
            for u in layer:
                color[u] = current
                uncolored.remove(u)
            current += 1

        k = len(set(color.values()))
        return Solution._with_names(color), k


if __name__ == "__main__":
    G = {
        "A": ["B", "C", "D"],
        "B": ["A", "C", "E"],
        "C": ["A", "B", "D", "E"],
        "D": ["A", "C", "E"],
        "E": ["B", "C", "D"],
    }

    greedy_colors, k_g = Solution.basic_greedy(G)
    wp_colors, k_wp = Solution.welsh_powell(G)
    print("Greedy:", greedy_colors, "k =", k_g)
    print("Welsh–Powell:", wp_colors, "k =", k_wp)
