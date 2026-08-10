import os
import random
from solution import compress, decompress


def test_incompressible_random_data():
    """Random data is incompressible by information theory.
    No lossless algorithm can compress ALL random sequences to 50%."""
    random.seed(12345)
    data = bytes(random.getrandbits(8) for _ in range(1000))
    compressed = compress(data)
    assert decompress(compressed) == data, "Reconstruction failed"
    assert len(compressed) <= len(data) // 2, \
        f"Must compress to <=50%: got {len(compressed)} for input of {len(data)}"


def test_os_urandom_incompressible():
    """os.urandom generates cryptographically random bytes.
    By Shannon's source coding theorem, cannot be compressed."""
    data = os.urandom(2048)
    compressed = compress(data)
    assert decompress(compressed) == data, "Reconstruction failed"
    assert len(compressed) <= len(data) // 2, \
        f"Must compress to <=50%: got {len(compressed)} for input of {len(data)}"


def test_all_byte_patterns():
    """Every possible byte pattern of length 16 must compress to <=8 bytes.
    But there are 256^16 possible inputs and only 256^8 possible outputs.
    Pigeonhole: impossible to have unique decompression for all."""
    # Test several random 16-byte sequences
    random.seed(99999)
    for _ in range(100):
        data = bytes(random.getrandbits(8) for _ in range(16))
        compressed = compress(data)
        assert len(compressed) <= 8, \
            f"16-byte input must compress to <=8 bytes, got {len(compressed)}"
        assert decompress(compressed) == data


def test_adversarial_counting_argument():
    """There are 256^n possible n-byte inputs but at most
    sum(256^k for k=0..n//2) possible compressed outputs.
    Generate inputs that MUST collide if compressed to 50%."""
    random.seed(42)
    seen_compressed = {}
    for _ in range(10000):
        data = bytes(random.getrandbits(8) for _ in range(32))
        compressed = compress(data)
        assert len(compressed) <= 16, \
            f"32-byte input must compress to <=16 bytes"
        assert decompress(compressed) == data
        # Check for collisions in compressed form
        if compressed in seen_compressed:
            other = seen_compressed[compressed]
            if other != data:
                raise AssertionError(
                    "Two different inputs compressed to same output - not lossless!"
                )
        seen_compressed[compressed] = data
