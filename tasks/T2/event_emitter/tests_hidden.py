from solution import EventEmitter


def test_multiple_listeners_order_preserved():
    """Invariant: listeners fire in registration order."""
    ee = EventEmitter()
    results = []
    ee.on("event", lambda: results.append("first"))
    ee.on("event", lambda: results.append("second"))
    ee.on("event", lambda: results.append("third"))
    ee.emit("event")
    assert results == ["first", "second", "third"]


def test_removal_during_emit_does_not_skip():
    """Invariant: removing a listener during emit doesn't affect current emission."""
    ee = EventEmitter()
    results = []

    def remove_self():
        results.append("A")
        ee.off("event", remove_self)

    def listener_b():
        results.append("B")

    ee.on("event", remove_self)
    ee.on("event", listener_b)
    ee.emit("event")
    assert results == ["A", "B"]
    # Second emit: remove_self was removed
    results.clear()
    ee.emit("event")
    assert results == ["B"]


def test_off_removes_only_one_registration():
    """Invariant: off removes exactly one registration, not all."""
    ee = EventEmitter()
    results = []
    cb = lambda: results.append(1)
    ee.on("x", cb)
    ee.on("x", cb)
    ee.on("x", cb)
    ee.off("x", cb)
    ee.emit("x")
    assert results == [1, 1]  # two remain


def test_off_nonexistent_listener_no_error():
    """Invariant: removing a non-registered callback is a no-op."""
    ee = EventEmitter()
    ee.off("no_event", lambda: None)  # should not raise


def test_once_with_multiple_listeners():
    """Invariant: once only removes the once-listener, others remain."""
    ee = EventEmitter()
    results = []
    ee.on("ev", lambda: results.append("persistent"))
    ee.once("ev", lambda: results.append("one-shot"))
    ee.emit("ev")
    assert results == ["persistent", "one-shot"]
    results.clear()
    ee.emit("ev")
    assert results == ["persistent"]


def test_emit_passes_args_and_kwargs():
    """Invariant: all positional and keyword args are forwarded."""
    ee = EventEmitter()
    received = []
    ee.on("data", lambda *a, **kw: received.append((a, kw)))
    ee.emit("data", 1, 2, key="val")
    assert received == [((1, 2), {"key": "val"})]


def test_separate_events_are_independent():
    """Invariant: listeners on different events don't interfere."""
    ee = EventEmitter()
    a_results = []
    b_results = []
    ee.on("a", lambda: a_results.append(1))
    ee.on("b", lambda: b_results.append(2))
    ee.emit("a")
    assert a_results == [1]
    assert b_results == []


def test_once_listener_removed_after_first_emit_only():
    """Invariant: once listener doesn't fire on subsequent emits even in complex scenarios."""
    ee = EventEmitter()
    call_count = []

    def counter():
        call_count.append(1)

    ee.once("tick", counter)
    ee.on("tick", lambda: None)  # another listener to keep event active
    ee.emit("tick")
    ee.emit("tick")
    ee.emit("tick")
    assert len(call_count) == 1
