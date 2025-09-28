# Complejidades:
# Construcción de frecuencias: O(n)  donde n = longitud del texto
# Construcción del árbol de Huffman: O(m log m)  donde m = número de caracteres distintos
# Generación de códigos: O(m)
# Codificación del texto: O(n)
# Decodificación del texto: O(n)
# Espacio: O(m + n)

from queue import PriorityQueue
from collections import Counter
import json
import os

class Nodo:
    def __init__(self, caracter, prob):
        self.caracter = caracter
        self.prob = prob
        self.tag = -1
        self.right = -1
        self.left  = -1

class Arbol:
    def __init__ (self, raiz):
        self.raiz = raiz

    def show(self):
        self.preorder(self.raiz)

    def preorder(self, node, pref=""):
        print(f"{pref}{node.prob:.6f}\t{repr(node.caracter)}")
        if node.left != -1:
            self.preorder(node.left,  pref + "  ")
        if node.right != -1:
            self.preorder(node.right, pref + "  ")

    def _build_codes(self, node, prefix, out):
        if node.left == -1 and node.right == -1:
            out[node.caracter] = prefix if prefix else "0"
            return
        if node.left  != -1: self._build_codes(node.left,  prefix + "0", out)
        if node.right != -1: self._build_codes(node.right, prefix + "1", out)

    def code_map(self):
        codes = {}
        self._build_codes(self.raiz, "", codes)
        return codes

class HuffmanCodes:
    @staticmethod
    def normalize(s):
        replacements = (
            ("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"),
            ("Á", "A"), ("É", "E"), ("Í", "I"), ("Ó", "O"), ("Ú", "U"),
        )
        for a, b in replacements:
            s = s.replace(a, b)
        return s

    @staticmethod
    def process_txt(path: str) -> str:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        return HuffmanCodes.normalize(text)

    @staticmethod
    def get_probabilities(path: str, include_whitespace: bool = True):
        text = HuffmanCodes.process_txt(path)
        if not include_whitespace:
            text = "".join(ch for ch in text if not ch.isspace())
        counts = Counter(text)
        total = sum(counts.values()) or 1
        characters   = list(counts.keys())
        probabilities = [counts[ch] / total for ch in characters]
        return characters, probabilities, dict(counts), {ch: counts[ch]/total for ch in counts}

    @staticmethod
    def create_tree(path: str, include_whitespace: bool = True):
        chars, probs, counts, prob_map = HuffmanCodes.get_probabilities(path, include_whitespace)
        tree = crea_huffman_tree(chars, probs)
        codes = tree.code_map()
        return tree, codes, counts, prob_map

    @staticmethod
    def show_tree(tree: Arbol):
        tree.show()

    @staticmethod
    def encode_text(text: str, codes: dict, include_whitespace: bool = True) -> str:
        text = HuffmanCodes.normalize(text)
        if not include_whitespace:
            text = "".join(ch for ch in text if not ch.isspace())
        return "".join(codes[ch] for ch in text)

    @staticmethod
    def decode_text(bits: str, codes: dict) -> str:
        inv = {v: k for k, v in codes.items()}
        out, cur = [], ""
        for b in bits:
            cur += b
            if cur in inv:
                out.append(inv[cur])
                cur = ""
        return "".join(out)

    @staticmethod
    def encoding_summary(counts: dict, probs: dict, codes: dict):
        rows = []
        for ch, cnt in counts.items():
            rows.append((repr(ch)[1:-1], cnt, probs[ch], codes[ch]))
        rows.sort(key=lambda r: (-r[1], r[0]))
        for ch, cnt, p, code in rows:
            print(f"{ch}\t{cnt}\t{p:.6f}\t{code}")

    MAGIC = b"HUF1"

    @staticmethod
    def save_bin(dst_bin: str, codes: dict, payload_bits: str):
        code_json = json.dumps(codes, ensure_ascii=False).encode("utf-8")
        bit_len = len(payload_bits)
        pad = (8 - (bit_len % 8)) % 8
        bits_padded = payload_bits + ("0" * pad)
        data = bytearray()
        for i in range(0, len(bits_padded), 8):
            data.append(int(bits_padded[i:i+8], 2))
        with open(dst_bin, "wb") as f:
            f.write(HuffmanCodes.MAGIC)
            f.write(len(code_json).to_bytes(4, "big"))
            f.write(code_json)
            f.write(bit_len.to_bytes(4, "big"))
            f.write(bytes(data))

    @staticmethod
    def load_bin(src_bin: str):
        with open(src_bin, "rb") as f:
            mg = f.read(4)
            if mg != HuffmanCodes.MAGIC:
                raise ValueError("MAGIC inválido")
            code_len = int.from_bytes(f.read(4), "big")
            code_json = f.read(code_len)
            codes = json.loads(code_json.decode("utf-8"))
            bit_len = int.from_bytes(f.read(4), "big")
            payload = f.read()
        bits = "".join(f"{b:08b}" for b in payload)[:bit_len]
        return codes, bits

_tie_ctr = 0
def min_probs(arboles: PriorityQueue):
    a = arboles.get()[2]
    b = arboles.get()[2]
    return [a, b]

def merge_trees(a: Arbol, b: Arbol):
    raiz_nuevo = Nodo(caracter="", prob=a.raiz.prob + b.raiz.prob)
    raiz_nuevo.left  = a.raiz
    raiz_nuevo.right = b.raiz
    raiz_nuevo.left.tag  = 0
    raiz_nuevo.right.tag = 1
    return Arbol(raiz_nuevo)

def crea_huffman_tree(caracteres, probabilidades):
    global _tie_ctr
    arboles = PriorityQueue()
    n = len(probabilidades)
    for i in range(n):
        node = Nodo(caracteres[i], probabilidades[i])
        arboles.put( (node.prob, _tie_ctr, Arbol(node)) )
        _tie_ctr += 1
    while arboles.qsize() > 1:
        min_A, min_B = min_probs(arboles)
        arbol_fusionado = merge_trees(min_A, min_B)
        arboles.put( (arbol_fusionado.raiz.prob, _tie_ctr, arbol_fusionado) )
        _tie_ctr += 1
    return arboles.get()[2]

def menu():
    print("\n===== Huffman Menu =====")
    print("0) Construir árbol desde .txt")
    print("1) Codificar archivo .txt -> .bin")
    print("2) Decodificar archivo .bin -> .txt")
    print("3) Mostrar tabla (char, ocurrencias, prob, código)")
    print("4) Codificar texto ingresado")
    print("5) Decodificar bits ingresados")
    print("6) Mostrar árbol (preorden)")
    print("7) Mostrar códigos para: escalera, sitio, pie, suelo")
    print("9) Salir")

def main():
    tree = None
    codes = None
    counts = None
    probs = None
    include_ws = True

    while True:
        menu()
        op = input("> ").strip()

        if op == "9":
            print("Bye.")
            return

        try:
            if op == "0":
                path = input("Ruta .txt corpus: ").strip()
                incl = input("¿Incluir espacios? (y/n) [y]: ").strip().lower() or "y"
                include_ws = (incl != "n")
                tree, codes, counts, probs = HuffmanCodes.create_tree(path, include_ws)
                print("Árbol construido.")

            elif op == "1":
                src = input("Ruta .txt a codificar: ").strip()
                dst = input("Salida .bin: ").strip()
                text = HuffmanCodes.process_txt(src)
                if not include_ws:
                    text = "".join(ch for ch in text if not ch.isspace())
                bits = HuffmanCodes.encode_text(text, codes, include_ws)
                HuffmanCodes.save_bin(dst, codes, bits)
                print("Archivo codificado:", dst)

            elif op == "2":
                src = input("Ruta .bin: ").strip()
                dst = input("Salida .txt: ").strip()
                file_codes, bits = HuffmanCodes.load_bin(src)
                text = HuffmanCodes.decode_text(bits, file_codes)
                with open(dst, "w", encoding="utf-8") as f:
                    f.write(text)
                print("Archivo decodificado:", dst)

            elif op == "3":
                HuffmanCodes.encoding_summary(counts, probs, codes)

            elif op == "4":
                s = input("Texto: ")
                bits = HuffmanCodes.encode_text(s, codes, include_ws)
                print("Bits:", bits)

            elif op == "5":
                b = input("Bits: ").strip()
                txt = HuffmanCodes.decode_text(b, codes)
                print("Texto:", txt)

            elif op == "6":
                HuffmanCodes.show_tree(tree)

            elif op == "7":
                for w in ["escalera", "sitio", "pie", "suelo"]:
                    code = HuffmanCodes.encode_text(w, codes, include_ws)
                    print(f"{w}: {code}")

            else:
                print("Opción inválida.")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()

