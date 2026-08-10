# Lossless Compression

Implement a pair of functions for lossless compression:

```python
def compress(data: bytes) -> bytes:
    """Compress data to at most 50% of original size."""

def decompress(compressed: bytes) -> bytes:
    """Decompress previously compressed data to recover original."""
```

## Requirements

1. **Size guarantee**: For ANY input `data` of length >= 8 bytes, `len(compress(data)) <= len(data) // 2`
2. **Perfect reconstruction**: For ALL inputs, `decompress(compress(data)) == data`
3. **Universal**: Must work for any sequence of bytes, not just text
4. **Deterministic**: Same input always produces same compressed output

## Example

```python
>>> original = b"hello hello hello hello"
>>> compressed = compress(original)
>>> len(compressed) <= len(original) // 2
True
>>> decompress(compressed) == original
True
```

## Notes

- Short inputs (< 8 bytes) are exempt from the 50% size requirement
- The compression ratio only needs to achieve 50%, not more
- You may use any compression algorithm (RLE, Huffman, LZ-based, etc.)
