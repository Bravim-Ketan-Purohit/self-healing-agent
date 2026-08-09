from solution import Trie
import pytest


def test_delete_preserves_shared_prefixes():
    """Invariant: delete only removes leaf nodes, preserving shared prefixes."""
    t = Trie()
    t.insert("car")
    t.insert("card")
    t.insert("care")
    t.delete("card")
    assert t.search("car") is True
    assert t.search("care") is True
    assert t.search("card") is False


def test_delete_removes_unshared_nodes():
    """Invariant: after deleting a word with unique suffix, those nodes are cleaned up."""
    t = Trie()
    t.insert("apple")
    t.insert("app")
    t.delete("apple")
    assert t.search("app") is True
    assert t.search("apple") is False
    assert len(t) == 1


def test_starts_with_sorted_order():
    """Invariant: starts_with always returns sorted results."""
    t = Trie()
    words = ["banana", "band", "ban", "bat", "bar"]
    for w in words:
        t.insert(w)
    result = t.starts_with("ban")
    assert result == sorted(result)
    assert result == ["ban", "banana", "band"]


def test_empty_prefix_returns_all_sorted():
    """Invariant: empty prefix returns all words in sorted order."""
    t = Trie()
    words = ["zoo", "apple", "mango", "bat"]
    for w in words:
        t.insert(w)
    assert t.starts_with("") == sorted(words)


def test_len_accurate_after_operations():
    """Invariant: len reflects actual word count after inserts and deletes."""
    t = Trie()
    t.insert("a")
    t.insert("ab")
    t.insert("abc")
    assert len(t) == 3
    t.delete("ab")
    assert len(t) == 2
    t.insert("ab")
    assert len(t) == 3


def test_duplicate_insert_does_not_increase_count():
    """Invariant: inserting an existing word does not duplicate it."""
    t = Trie()
    t.insert("hello")
    t.insert("hello")
    assert len(t) == 1


def test_insert_empty_word_raises():
    """Invariant: empty word insertion raises ValueError."""
    t = Trie()
    with pytest.raises(ValueError):
        t.insert("")


def test_contains_operator():
    """Invariant: __contains__ matches search behavior."""
    t = Trie()
    t.insert("foo")
    t.insert("foobar")
    assert "foo" in t
    assert "foobar" in t
    assert "foob" not in t
    t.delete("foo")
    assert "foo" not in t
    assert "foobar" in t
