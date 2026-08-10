# Huffman Encoder & Decoder

## Problem

Implement two classes that work together to compress and decompress text:

1. **`HuffmanEncoder`** - Compresses a text string:
   - `__init__(self, text)` - Takes the text to compress.
   - `encode()` - Returns a tuple `(encoded_bits, tree_data)`:
     - `encoded_bits`: a string of '0' and '1' characters representing the compressed data.
     - `tree_data`: any serializable representation of the Huffman tree needed for decoding.

2. **`HuffmanDecoder`** - Decompresses encoded data:
   - `__init__(self, tree_data)` - Takes the tree data from the encoder.
   - `decode(encoded_bits)` - Returns the original text string.

## Interface Contract

- `HuffmanDecoder(tree_data).decode(encoded_bits)` must produce the original text when given the outputs of `HuffmanEncoder(text).encode()`.
- The encoder must build a Huffman tree based on character frequencies.
- The tree_data format is shared between encoder and decoder—they must agree on it.
- Single-character strings must work (edge case: only one unique character).
- Empty string can either be handled or raise a ValueError.

## Example

```python
encoder = HuffmanEncoder("hello world")
encoded_bits, tree_data = encoder.encode()
decoder = HuffmanDecoder(tree_data)
assert decoder.decode(encoded_bits) == "hello world"
```

## Constraints

- Do NOT use any compression library (zlib, gzip, etc.).
- Both classes must be in the same `solution.py` file.
