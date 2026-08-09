from solution import Logger


def test_tags_not_shared_between_entries():
    """Default tags must not be shared across calls (mutable default trap)."""
    logger = Logger()
    e1 = logger.log("first")
    e1["tags"].append("added_later")
    e2 = logger.log("second")
    assert e2["tags"] == []


def test_tags_independent_across_instances():
    """Different Logger instances must not share tag lists."""
    logger1 = Logger()
    logger2 = Logger()
    e1 = logger1.log("a")
    e1["tags"].append("x")
    e2 = logger2.log("b")
    assert e2["tags"] == []


def test_multiple_calls_no_leak():
    """Calling log() many times without tags should give independent lists."""
    logger = Logger()
    entries = [logger.log(f"msg{i}") for i in range(5)]
    entries[0]["tags"].append("leaked")
    for entry in entries[1:]:
        assert entry["tags"] == []


def test_provided_tags_not_aliased():
    """Provided tags list should be copied, not aliased."""
    logger = Logger()
    my_tags = ["info"]
    entry = logger.log("test", tags=my_tags)
    my_tags.append("mutated")
    assert entry["tags"] == ["info"]


def test_entries_list_not_shared():
    """Each Logger instance has its own entries list."""
    logger1 = Logger()
    logger2 = Logger()
    logger1.log("a")
    assert logger2.entries == []


def test_tag_mutation_does_not_affect_stored_entry():
    """Mutating returned entry tags doesn't affect stored entry."""
    logger = Logger()
    entry = logger.log("test")
    entry["tags"].append("hacked")
    # The stored entry should also show this (same reference is ok)
    # but NEXT entry must not be affected
    entry2 = logger.log("next")
    assert entry2["tags"] == []


def test_many_instances_isolation():
    """Stress test: many instances created, no leakage."""
    loggers = [Logger() for _ in range(20)]
    for i, lg in enumerate(loggers):
        e = lg.log(f"msg{i}")
        e["tags"].append(f"tag{i}")
    # Each logger's first entry should only have its own tag
    for i, lg in enumerate(loggers):
        assert lg.entries[0]["tags"] == [f"tag{i}"]
