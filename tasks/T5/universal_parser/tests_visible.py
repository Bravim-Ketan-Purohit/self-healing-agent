from solution import parse


def test_simple_grammar():
    grammar = "S -> a S b | a b"
    assert parse(grammar, "ab") == True
    assert parse(grammar, "aabb") == True
    assert parse(grammar, "aaabbb") == True
    assert parse(grammar, "aab") == False


def test_alternation():
    grammar = "S -> a | b | c"
    assert parse(grammar, "a") == True
    assert parse(grammar, "b") == True
    assert parse(grammar, "d") == False


def test_recursive():
    grammar = "S -> a S | a"
    assert parse(grammar, "a") == True
    assert parse(grammar, "aaa") == True
    assert parse(grammar, "b") == False


def test_multiple_nonterminals():
    grammar = "S -> A B\nA -> a | a A\nB -> b | b B"
    assert parse(grammar, "ab") == True
    assert parse(grammar, "aaabbb") == True
    assert parse(grammar, "ba") == False
