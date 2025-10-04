from collections import defaultdict

# ---------------------------
# 1) TRIE de diccionario
# ---------------------------
class TrieNode:
    __slots__ = ("children", "end")
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.end: bool = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        cur = self.root
        for ch in word:
            if ch not in cur.children:
                cur.children[ch] = TrieNode()
            cur = cur.children[ch]
        cur.end = True

    def _collect(self, node: TrieNode, prefix: str, out: list[str]) -> None:
        if node.end:
            out.append(prefix)
        for ch, nxt in node.children.items():
            self._collect(nxt, prefix + ch, out)

    def autocomplete(self, prefix: str) -> list[str]:
        """
        Si prefix existe COMPLETO (end=True), imprime ese mensaje.
        Si solo existe parcialmente, devuelve opciones para autocompletar.
        Si no existe, devuelve lista vacia.
        """
        cur = self.root
        for ch in prefix:
            if ch not in cur.children:
                # no existe ni parcialmente
                return []
            cur = cur.children[ch]

        # Existe el camino del prefijo
        if cur.end:
            print(f"La cadena {prefix} existe completa")
        # Recolectar todas las continuaciones desde el nodo del prefijo
        opciones: list[str] = []
        self._collect(cur, prefix, opciones)
        # Si el prefijo mismo es palabra, puedes querer excluirlo de las sugerencias:
        # opciones_sin_prefijo = [w for w in opciones if w != prefix]
        return opciones

# ---------------------------
# 2) TRIE de sufijos
# ---------------------------
class SuffixTrieNode:
    __slots__ = ("children", "indices")
    def __init__(self):
        self.children: dict[str, SuffixTrieNode] = {}
        # Guardamos indices de inicio de sufijos que pasan por este nodo
        self.indices: list[int] = []

class SuffixTrie:
    def __init__(self, text: str):
        self.text = text
        self.root = SuffixTrieNode()
        self._build()

    def _insert_suffix(self, start_idx: int) -> None:
        cur = self.root
        cur.indices.append(start_idx)
        for ch in self.text[start_idx:]:
            if ch not in cur.children:
                cur.children[ch] = SuffixTrieNode()
            cur = cur.children[ch]
            cur.indices.append(start_idx)

    def _build(self) -> None:
        for i in range(len(self.text)):
            self._insert_suffix(i)

    def search(self, pattern: str) -> list[tuple[int, int]]:
        """
        Devuelve [(inicio, fin)] de todas las ocurrencias del patron.
        """
        cur = self.root
        for ch in pattern:
            if ch not in cur.children:
                return []
            cur = cur.children[ch]
        # Todas las posiciones donde comienza el patron
        L = len(pattern)
        return [(i, i + L - 1) for i in cur.indices]

# ---------------------------
# DEMO con datos del enunciado
# ---------------------------
if __name__ == "__main__":
    # Palabras del diccionario
    palabras = [
        "casi", "casa", "cama", "camisa", "camara", "camion",
        "ave", "alce"
    ]

    trie = Trie()
    for w in palabras:
        trie.insert(w)

    print("=== Autocompletar ===")
    # Caso exacto
    _ = trie.autocomplete("casa")  # imprime existencia
    # Caso parcial
    opciones_cam = trie.autocomplete("cam")
    # Ejemplo esperado: camara, camion, camisa (el orden puede variar segun insercion)
    print("Opciones para 'cam':", opciones_cam)

    # Otros ejemplos breves
    print("Opciones para 'ca':", trie.autocomplete("ca"))
    print("Opciones para 'al':", trie.autocomplete("al"))
    print("Opciones para 'z':", trie.autocomplete("z"))  # inexistente

    print("\n=== Suffix trie ===")
    texto = "anabanana"
    st = SuffixTrie(texto)

    def prueba_patron(p: str):
        occ = st.search(p)
        print(f"Patron '{p}' -> ocurrencias: {occ}")
        # Mostrar subcadenas
        for (i, j) in occ:
            print(f"  '{texto[i:j+1]}' en [{i}, {j}]")

    # Casos de prueba
    prueba_patron("ana")  # esperado: (0,2), (4,6), (6,8)
    prueba_patron("ban")  # esperado: (3,5)
    prueba_patron("nana") # esperado: (5,8)
    prueba_patron("x")    # esperado: []
