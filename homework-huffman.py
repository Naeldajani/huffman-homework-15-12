

#exercise 1

def frequency(texte: str) -> dict[str, int]:
    texte = texte.lower()
    dictionnaire = {}
    for letter in texte:
        if letter not in dictionnaire.keys():
            dictionnaire[letter] = 1
        else:
            dictionnaire[letter] += 1
    return dictionnaire
    
from heapq import heappush, heappop, heapify

class Node:
    def __init__(self, characters: str, frequency: int):
        self.characters = characters
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other: "Node") -> bool:
        return self.frequency < other.frequency

#exercise 3

def huffman_tree(freqs: dict[str, int]) -> Node:
    if not freqs:
        return None

    if len(freqs) == 1:
        characters, frequences = list(freqs.items())[0]
        return Node(characters, frequences)

    heap = []
    for characters, freq in freqs.items():
        node = Node(characters, freq)
        heappush(heap, node)

    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)

        combined_characters = left.characters + right.characters
        combined_frequences = left.frequency + right.frequency
        parent = Node(combined_characters, combined_frequences)
        parent.left = left
        parent.right = right

        heappush(heap, parent)

    return heap[0]

#exercise 4

def get_code(tree: Node, char: str) -> str:
    def search(node, target, path=""):
        if node is None:
            return None

        if node.left is None and node.right is None:
            if target in node.characters:
                return path
            else:
                return None

        if node.left:
            resultat = search(node.left, target, path + "0")
            if resultat is not None:
                return resultat

        if node.right:
            resultat = search(node.right, target, path + "1")
            if resultat is not None:
                return resultat

        return None

    result = search(tree, char)
    if result is None:
        raise ValueError(f"Character '{char}' not found in tree")
    return result

#exercise 5

def show_all_codes(tree: Node) -> None:
    if tree is None:
        return

    characters = set(tree.characters)

    for index in sorted(characters):
        code = get_code(tree, index)
        print(f"Character: {index} Code: {code}")

#exercise 6

def huffman_encode(texte: str, tree: Node) -> str:
    texte = texte.lower()

    u = ""
    for lettre in texte:
        code = get_code(tree, lettre)
        u += code

    return u

def huffman_decode(u_texte: str, tree: Node) -> str:
    if not u_texte or tree is None:
        return ""

    v = ""
    current = tree

    for bit in u_texte:
        if bit == '0':
            current = current.left
        else:
            current = current.right

        if current.left is None and current.right is None:
            v += current.characters
            current = tree

    return v

#exercise 7

freqs_english = {
" ": 18.0,
"e": 12.02, "t": 9.10, "a": 8.12, "o": 7.68, "i": 7.31, "n": 6.95,
"s": 6.28, "r": 6.02, "h": 5.92, "d": 4.32, "l": 3.98, "u": 2.88,
"c": 2.71, "m": 2.61, "f": 2.30, "y": 2.11, "w": 2.09, "g": 2.03,
"p": 1.82, "b": 1.49, "v": 1.11, "k": 0.69, "x": 0.17, "q": 0.11,
"j": 0.10, "z": 0.07
}

english_tree = huffman_tree(freqs_english)

test_text = "huffman coding is a data compression algorithm"
encoded = huffman_encode(test_text, english_tree)
decoded = huffman_decode(encoded, english_tree)

print("Test text:",test_text)
print("Encoded length:",len(encoded), "bits")
print("Original length:",len(test_text) * 8, "bits")
print("Compression ratio:", round((1 - len(encoded)/(len(test_text)*8))*100, 1), "%")

print("Decoded matches original:", decoded == test_text.lower())
