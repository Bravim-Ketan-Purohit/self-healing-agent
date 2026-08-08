# Group Anagrams

Write a function `group_anagrams(strs: list[str]) -> list[list[str]]` that groups a list of strings by anagram equivalence.

Two strings are anagrams if they contain the same characters with the same frequencies.

Return a list of groups, where each group is a list of strings that are anagrams of each other. The groups may be in any order, and the strings within each group may be in any order.

## Constraints

- `strs` may be empty.
- Strings contain only lowercase English letters.
- Strings may be empty (empty strings are anagrams of each other).

## Examples

```python
group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
# => [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]] (order may vary)

group_anagrams([""])
# => [[""]]

group_anagrams(["a"])
# => [["a"]]
```
