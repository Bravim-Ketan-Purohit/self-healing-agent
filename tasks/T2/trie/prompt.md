# Trie

Implement a `Trie` class (prefix tree) with the following operations:

- `__init__(self)` — Create an empty trie.
- `insert(self, word: str) -> None` — Insert a word into the trie. Raises `ValueError` if word is empty.
- `search(self, word: str) -> bool` — Return True if the exact word exists in the trie.
- `starts_with(self, prefix: str) -> list[str]` — Return a sorted list of all words that start with the given prefix.
- `delete(self, word: str) -> None` — Remove a word from the trie. Raises `KeyError` if word is not found. Only removes nodes that are no longer needed (leaf nodes with no children and not marking another word's end).
- `__len__(self) -> int` — Return the number of words in the trie.
- `__contains__(self, word: str) -> bool` — Return True if word is in the trie.

## Invariants

- Delete only removes nodes that are no longer shared by other words.
- After deletion, all remaining words must still be searchable.
- `starts_with` always returns results in sorted order.

## Examples

```python
t = Trie()
t.insert("cat")
t.insert("car")
t.insert("card")
t.search("car")      # True
t.search("ca")       # False
t.starts_with("ca")  # ["car", "card", "cat"]
t.delete("car")
t.search("car")      # False
t.search("card")     # True (not affected)
len(t)               # 2
```
