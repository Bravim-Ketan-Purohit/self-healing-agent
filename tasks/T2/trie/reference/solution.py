class _TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    """Prefix tree with insert, search, starts_with, and delete."""

    def __init__(self):
        self._root = _TrieNode()
        self._size = 0

    def insert(self, word: str) -> None:
        if not word:
            raise ValueError("Word must not be empty")
        node = self._root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = _TrieNode()
            node = node.children[ch]
        if not node.is_end:
            node.is_end = True
            self._size += 1

    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> list:
        node = self._find_node(prefix)
        if node is None:
            return []
        results = []
        self._collect(node, prefix, results)
        return sorted(results)

    def delete(self, word: str) -> None:
        if not self.search(word):
            raise KeyError(f"Word '{word}' not found in trie")
        self._delete_recursive(self._root, word, 0)
        self._size -= 1

    def _delete_recursive(self, node: _TrieNode, word: str, depth: int) -> bool:
        if depth == len(word):
            node.is_end = False
            return len(node.children) == 0
        ch = word[depth]
        child = node.children[ch]
        should_delete = self._delete_recursive(child, word, depth + 1)
        if should_delete:
            del node.children[ch]
            return not node.is_end and len(node.children) == 0
        return False

    def _find_node(self, prefix: str) -> _TrieNode:
        node = self._root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def _collect(self, node: _TrieNode, prefix: str, results: list) -> None:
        if node.is_end:
            results.append(prefix)
        for ch in sorted(node.children):
            self._collect(node.children[ch], prefix + ch, results)

    def __len__(self) -> int:
        return self._size

    def __contains__(self, word: str) -> bool:
        return self.search(word)
