# Immutable Mutator

Implement a class `FrozenList` that behaves like a truly immutable list but supports an `append` method.

## Requirements

1. **Immutability**: Once created, the FrozenList's contents never change. Any attempt to modify should raise `TypeError`
2. **Append method**: `append(value)` returns a **new** FrozenList with the value added at the end
3. **Identity preservation**: The original FrozenList is completely unchanged after append (same `id()`, same contents)
4. **Indexing**: Supports `__getitem__`, `__len__`, and `__iter__`
5. **Hashable**: Since it's immutable, it should be hashable (support `__hash__`)
6. **Equality**: Two FrozenLists with same contents should be equal

## Example

```python
>>> fl = FrozenList([1, 2, 3])
>>> fl2 = fl.append(4)
>>> list(fl)
[1, 2, 3]
>>> list(fl2)
[1, 2, 3, 4]
>>> fl is not fl2
True
>>> hash(fl)  # works because immutable
# some integer
```

## API

```python
class FrozenList:
    def __init__(self, items=None):
        """Create a FrozenList from an iterable."""
    
    def append(self, value) -> 'FrozenList':
        """Return a new FrozenList with value appended."""
    
    def __getitem__(self, index):
        """Access by index."""
    
    def __len__(self):
        """Return length."""
    
    def __iter__(self):
        """Iterate over items."""
    
    def __hash__(self):
        """Hash (immutable so this is safe)."""
    
    def __eq__(self, other):
        """Equality comparison."""
```
