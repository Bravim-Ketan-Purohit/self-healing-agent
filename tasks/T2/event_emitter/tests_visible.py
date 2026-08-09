from solution import EventEmitter


def test_on_and_emit():
    ee = EventEmitter()
    results = []
    ee.on("data", lambda x: results.append(x))
    ee.emit("data", 42)
    assert results == [42]


def test_off_removes_listener():
    ee = EventEmitter()
    results = []
    cb = lambda x: results.append(x)
    ee.on("data", cb)
    ee.off("data", cb)
    ee.emit("data", 99)
    assert results == []


def test_once_fires_once():
    ee = EventEmitter()
    results = []
    ee.once("ping", lambda: results.append(1))
    ee.emit("ping")
    ee.emit("ping")
    assert results == [1]


def test_emit_with_no_listeners():
    ee = EventEmitter()
    # Should not raise
    ee.emit("nothing")
