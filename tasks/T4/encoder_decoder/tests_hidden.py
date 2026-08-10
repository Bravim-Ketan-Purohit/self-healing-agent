import pytest
from solution import HuffmanEncoder, HuffmanDecoder


def test_single_character():
    text = "aaaa"
    encoder = HuffmanEncoder(text)
    bits, tree_data = encoder.encode()
    decoder = HuffmanDecoder(tree_data)
    assert decoder.decode(bits) == text


def test_two_chars():
    text = "ababab"
    encoder = HuffmanEncoder(text)
    bits, tree_data = encoder.encode()
    decoder = HuffmanDecoder(tree_data)
    assert decoder.decode(bits) == text


def test_long_text():
    text = "the quick brown fox jumps over the lazy dog"
    encoder = HuffmanEncoder(text)
    bits, tree_data = encoder.encode()
    decoder = HuffmanDecoder(tree_data)
    assert decoder.decode(bits) == text


def test_compression_occurs():
    text = "aaaaabbbcc"
    encoder = HuffmanEncoder(text)
    bits, _ = encoder.encode()
    # Huffman should compress: frequent chars get shorter codes
    # Worst case: 10 chars * 8 bits = 80, but we use bits not bytes
    # At minimum: not longer than 3 bits per char for 3 unique chars
    assert len(bits) < len(text) * 3


def test_special_characters():
    text = "hello\nworld\ttab  spaces!!!"
    encoder = HuffmanEncoder(text)
    bits, tree_data = encoder.encode()
    decoder = HuffmanDecoder(tree_data)
    assert decoder.decode(bits) == text


def test_all_unique_chars():
    text = "abcdefgh"
    encoder = HuffmanEncoder(text)
    bits, tree_data = encoder.encode()
    decoder = HuffmanDecoder(tree_data)
    assert decoder.decode(bits) == text


def test_empty_string_raises():
    with pytest.raises((ValueError, Exception)):
        HuffmanEncoder("")


def test_unicode_chars():
    text = "café résumé"
    encoder = HuffmanEncoder(text)
    bits, tree_data = encoder.encode()
    decoder = HuffmanDecoder(tree_data)
    assert decoder.decode(bits) == text
