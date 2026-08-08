# Longest Common Prefix

Write a function `longest_common_prefix(strs: list[str]) -> str` that finds the longest common prefix string amongst a list of strings.

If there is no common prefix, return an empty string `""`.

## Constraints

- `strs` may be empty.
- Strings may be empty.
- Strings contain only lowercase English letters.

## Examples

```python
longest_common_prefix(["flower", "flow", "flight"]) == "fl"
longest_common_prefix(["dog", "racecar", "car"]) == ""
longest_common_prefix(["interspecies", "interstellar", "interstate"]) == "inters"
longest_common_prefix([]) == ""
longest_common_prefix(["alone"]) == "alone"
```
