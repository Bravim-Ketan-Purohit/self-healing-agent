from solution import HuffmanEncoder, HuffmanDecoder


def test_roundtrip_basic():
    text = "hello world"
    encoder = HuffmanEncoder(text)
    bits, tree_data = encoder.encode()
    decoder = HuffmanDecoder(tree_data)
    assert decoder.decode(bits) == text


def test_encoded_is_binary_string():
    encoder = HuffmanEncoder("test")
    bits, _ = encoder.encode()
    assert all(c in "01" for c in bits)


def test_roundtrip_repeated_chars():
    text = "aaabbbccc"
    encoder = HuffmanEncoder(text)
    bits, tree_data = encoder.encode()
    decoder = HuffmanDecoder(tree_data)
    assert decoder.decode(bits) == text
