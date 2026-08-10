"""
Tokenizer and Parser for arithmetic expressions.

Token format (the shared contract):
  {"type": "NUMBER"|"PLUS"|"MINUS"|"MUL"|"DIV"|"LPAREN"|"RPAREN", "value": str}

Do NOT use eval(), exec(), or ast.
"""


class Tokenizer:
    """Splits a math expression string into tokens."""

    def __init__(self, expression):
        raise NotImplementedError

    def tokenize(self):
        """Return a list of token dicts with 'type' and 'value' keys."""
        raise NotImplementedError


class Parser:
    """Evaluates a list of tokens respecting operator precedence."""

    def __init__(self, tokens):
        raise NotImplementedError

    def evaluate(self):
        """Return the numerical result of the expression."""
        raise NotImplementedError
