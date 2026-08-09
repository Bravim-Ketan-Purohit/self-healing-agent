from solution import Logger


def test_basic_log():
    logger = Logger()
    entry = logger.log("hello")
    assert entry == {"msg": "hello", "tags": []}


def test_log_with_tags():
    logger = Logger()
    entry = logger.log("error", tags=["critical", "db"])
    assert entry == {"msg": "error", "tags": ["critical", "db"]}


def test_entries_stored():
    logger = Logger()
    logger.log("a")
    logger.log("b")
    assert len(logger.entries) == 2


def test_multiple_logs():
    logger = Logger()
    e1 = logger.log("first")
    e2 = logger.log("second", tags=["info"])
    assert e1["msg"] == "first"
    assert e2["tags"] == ["info"]
