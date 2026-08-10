from solution import compress, decompress


def test_repetitive_text():
    data = b"aaaaaaaaaa" * 10  # 100 bytes of repetition
    compressed = compress(data)
    assert len(compressed) <= len(data) // 2
    assert decompress(compressed) == data


def test_natural_text():
    data = b"the quick brown fox jumps over the lazy dog " * 10
    compressed = compress(data)
    assert len(compressed) <= len(data) // 2
    assert decompress(compressed) == data


def test_short_input_exempt():
    data = b"short"
    compressed = compress(data)
    assert decompress(compressed) == data


def test_roundtrip_binary():
    data = bytes(range(256)) * 2
    compressed = compress(data)
    # Just verify lossless roundtrip (not compression ratio for binary)
    assert decompress(compressed) == data
