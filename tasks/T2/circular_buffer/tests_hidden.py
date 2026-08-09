from solution import CircularBuffer
import pytest


def test_fifo_order_after_wrap_around():
    """Invariant: items are always read in FIFO order even after wrap-around."""
    buf = CircularBuffer(3)
    buf.write(1)
    buf.write(2)
    buf.write(3)
    buf.read()  # consume 1
    buf.write(4)  # wraps around
    assert buf.read() == 2
    assert buf.read() == 3
    assert buf.read() == 4


def test_len_invariant():
    """Invariant: len reflects exact number of items at all times."""
    buf = CircularBuffer(3)
    assert len(buf) == 0
    buf.write("x")
    assert len(buf) == 1
    buf.write("y")
    assert len(buf) == 2
    buf.read()
    assert len(buf) == 1
    buf.write("a")
    buf.write("b")
    assert len(buf) == 3
    buf.read()
    buf.read()
    buf.read()
    assert len(buf) == 0


def test_overwrite_discards_oldest_only():
    """Invariant: overwrite replaces exactly the oldest item."""
    buf = CircularBuffer(3)
    buf.write("a")
    buf.write("b")
    buf.write("c")
    buf.overwrite("d")  # oldest was "a"
    buf.overwrite("e")  # oldest was "b"
    assert buf.read() == "c"
    assert buf.read() == "d"
    assert buf.read() == "e"


def test_overwrite_on_not_full_just_writes():
    """Invariant: overwrite when buffer is not full behaves like write."""
    buf = CircularBuffer(3)
    buf.overwrite(1)
    buf.overwrite(2)
    assert len(buf) == 2
    assert buf.read() == 1
    assert buf.read() == 2


def test_clear_resets_state():
    """Invariant: clear returns buffer to empty state."""
    buf = CircularBuffer(3)
    buf.write(1)
    buf.write(2)
    buf.write(3)
    buf.clear()
    assert len(buf) == 0
    with pytest.raises(BufferError):
        buf.read()
    # Can write again after clear
    buf.write(10)
    assert buf.read() == 10


def test_single_capacity_buffer():
    """Invariant: capacity-1 buffer works correctly for all operations."""
    buf = CircularBuffer(1)
    buf.write("only")
    assert len(buf) == 1
    with pytest.raises(BufferError):
        buf.write("extra")
    assert buf.read() == "only"
    assert len(buf) == 0
    buf.overwrite("new")
    buf.overwrite("newer")  # overwrites "new"
    assert buf.read() == "newer"


def test_capacity_validation():
    """Invariant: invalid capacity raises ValueError."""
    with pytest.raises(ValueError):
        CircularBuffer(0)
    with pytest.raises(ValueError):
        CircularBuffer(-5)


def test_many_write_read_cycles():
    """Invariant: buffer is correct through many full cycles."""
    buf = CircularBuffer(4)
    for cycle in range(10):
        for i in range(4):
            buf.write(cycle * 4 + i)
        for i in range(4):
            assert buf.read() == cycle * 4 + i
    assert len(buf) == 0
