# Title Case

Write a function `title_case(s: str) -> str` that converts a string to title case.

Title case means the first letter of each word is capitalized and the rest are lowercase. Words are separated by spaces. Apostrophes within words should not start a new capitalization (e.g., "don't" becomes "Don't", not "Don'T").

## Examples

```python
title_case("hello world") == "Hello World"
title_case("the quick brown fox") == "The Quick Brown Fox"
title_case("don't stop") == "Don't Stop"
title_case("") == ""
title_case("ALREADY UPPER") == "Already Upper"
```
