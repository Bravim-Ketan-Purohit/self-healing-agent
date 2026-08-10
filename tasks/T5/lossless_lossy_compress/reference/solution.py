import zlib


def compress(data: bytes) -> bytes:
    """Best attempt using zlib. Works for compressible data but fails
    on random/incompressible data where 50% ratio is impossible."""
    if len(data) < 8:
        return b'\x00' + data  # marker for uncompressed
    compressed = zlib.compress(data, level=9)
    # Always return compressed form; works for compressible data
    return compressed


def decompress(compressed: bytes) -> bytes:
    """Decompress data."""
    if not compressed:
        return b''
    if compressed[0:1] == b'\x00':
        return compressed[1:]
    try:
        return zlib.decompress(compressed)
    except zlib.error:
        return compressed
