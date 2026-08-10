"""Huffman Encoder and Decoder.

Do NOT use any compression library (zlib, gzip, etc.).
"""


class HuffmanEncoder:
    """Compresses text using Huffman coding."""

    def __init__(self, text):
        raise NotImplementedError

    def encode(self):
        """Return (encoded_bits, tree_data) tuple.

        encoded_bits: string of '0' and '1' characters
        tree_data: serializable representation of the Huffman tree
        """
        raise NotImplementedError


class HuffmanDecoder:
    """Decompresses Huffman-encoded data."""

    def __init__(self, tree_data):
        raise NotImplementedError

    def decode(self, encoded_bits):
        """Return the original text string from encoded bits."""
        raise NotImplementedError
