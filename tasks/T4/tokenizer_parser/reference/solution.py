"""
Tokenizer and Parser for arithmetic expressions.

Token format (the shared contract):
  {"type": "NUMBER"|"PLUS"|"MINUS"|"MUL"|"DIV"|"LPAREN"|"RPAREN", "value": str}
"""


class Tokenizer:
    """Splits a math expression string into tokens."""

    def __init__(self, expression):
        self.expression = expression

    def tokenize(self):
        """Return a list of token dicts with 'type' and 'value' keys."""
        tokens = []
        i = 0
        while i < len(self.expression):
            ch = self.expression[i]
            if ch.isspace():
                i += 1
            elif ch.isdigit() or ch == '.':
                start = i
                while i < len(self.expression) and (self.expression[i].isdigit() or self.expression[i] == '.'):
                    i += 1
                tokens.append({"type": "NUMBER", "value": self.expression[start:i]})
            elif ch == '+':
                tokens.append({"type": "PLUS", "value": "+"})
                i += 1
            elif ch == '-':
                tokens.append({"type": "MINUS", "value": "-"})
                i += 1
            elif ch == '*':
                tokens.append({"type": "MUL", "value": "*"})
                i += 1
            elif ch == '/':
                tokens.append({"type": "DIV", "value": "/"})
                i += 1
            elif ch == '(':
                tokens.append({"type": "LPAREN", "value": "("})
                i += 1
            elif ch == ')':
                tokens.append({"type": "RPAREN", "value": ")"})
                i += 1
            else:
                raise ValueError(f"Unexpected character: {ch}")
        return tokens


class Parser:
    """Evaluates a list of tokens respecting operator precedence.

    Grammar:
      expr   -> term ((PLUS | MINUS) term)*
      term   -> factor ((MUL | DIV) factor)*
      factor -> NUMBER | LPAREN expr RPAREN
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def evaluate(self):
        """Return the numerical result of the expression."""
        result = self._expr()
        return result

    def _current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _consume(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def _expr(self):
        result = self._term()
        while self._current() and self._current()["type"] in ("PLUS", "MINUS"):
            op = self._consume()
            right = self._term()
            if op["type"] == "PLUS":
                result = result + right
            else:
                result = result - right
        return result

    def _term(self):
        result = self._factor()
        while self._current() and self._current()["type"] in ("MUL", "DIV"):
            op = self._consume()
            right = self._factor()
            if op["type"] == "MUL":
                result = result * right
            else:
                result = result / right
        return result

    def _factor(self):
        token = self._current()
        if token["type"] == "NUMBER":
            self._consume()
            val = token["value"]
            return float(val) if '.' in val else int(val)
        elif token["type"] == "LPAREN":
            self._consume()  # consume '('
            result = self._expr()
            self._consume()  # consume ')'
            return result
        else:
            raise ValueError(f"Unexpected token: {token}")
