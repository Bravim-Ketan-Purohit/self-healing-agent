from solution import CircularBuffer
import pytest


def test_write_and_read():
    buf = CircularBuffer(3)
    buf.write("a")
    buf.write("b")
    assert buf.read() == "a"
    assert buf.read() == "b"


def test_read_empty_raises():
    buf = CircularBuffer(2)
    with pytest.raises(BufferError):
        buf.read()


def test_write_full_raises():
    buf = CircularBuffer(2)
    buf.write(1)
    buf.write(2)
    with pytest.raises(BufferError):
        buf.write(3)


def test_overwrite_when_full():
    buf = CircularBuffer(2)
    buf.write(1)
    buf.write(2)
    buf.overwrite(3)
    assert buf.read() == 2
    assert buf.read() == 3
