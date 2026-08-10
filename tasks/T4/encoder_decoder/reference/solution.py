"""Huffman Encoder and Decoder."""

import heapq
from collections import Counter


class _Node:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def _build_tree(text):
    freq = Counter(text)
    heap = [_Node(char=c, freq=f) for c, f in freq.items()]
    heapq.heapify(heap)

    if len(heap) == 1:
        # Single unique character: create a parent node
        node = heapq.heappop(heap)
        return _Node(freq=node.freq, left=node)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = _Node(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0]


def _build_codes(node, prefix="", codes=None):
    if codes is None:
        codes = {}
    if node is None:
        return codes
    if node.char is not None:
        codes[node.char] = prefix if prefix else "0"
        return codes
    _build_codes(node.left, prefix + "0", codes)
    _build_codes(node.right, prefix + "1", codes)
    return codes


def _serialize_tree(node):
    """Serialize the Huffman tree as a nested list structure."""
    if node is None:
        return None
    if node.char is not None:
        return ["leaf", node.char]
    return ["node", _serialize_tree(node.left), _serialize_tree(node.right)]


def _deserialize_tree(data):
    """Reconstruct the Huffman tree from serialized data."""
    if data is None:
        return None
    if data[0] == "leaf":
        return _Node(char=data[1])
    return _Node(left=_deserialize_tree(data[1]), right=_deserialize_tree(data[2]))


class HuffmanEncoder:
    """Compresses text using Huffman coding."""

    def __init__(self, text):
        if not text:
            raise ValueError("Cannot encode empty string")
        self.text = text

    def encode(self):
        """Return (encoded_bits, tree_data) tuple."""
        tree = _build_tree(self.text)
        codes = _build_codes(tree)
        encoded_bits = "".join(codes[ch] for ch in self.text)
        tree_data = _serialize_tree(tree)
        return encoded_bits, tree_data


class HuffmanDecoder:
    """Decompresses Huffman-encoded data."""

    def __init__(self, tree_data):
        self.root = _deserialize_tree(tree_data)

    def decode(self, encoded_bits):
        """Return the original text from encoded bits."""
        if self.root.char is not None:
            # Single character tree
            return self.root.char * len(encoded_bits)

        result = []
        node = self.root
        for bit in encoded_bits:
            if bit == "0":
                node = node.left
            else:
                node = node.right
            if node.char is not None:
                result.append(node.char)
                node = self.root
        return "".join(result)
