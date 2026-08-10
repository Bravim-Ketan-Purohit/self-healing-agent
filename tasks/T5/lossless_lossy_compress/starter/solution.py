def compress(data: bytes) -> bytes:
    """Compress data to at most 50% of original size (for inputs >= 8 bytes).
    Must be perfectly lossless for ALL inputs."""
    pass


def decompress(compressed: bytes) -> bytes:
    """Decompress previously compressed data to recover original exactly."""
    pass
