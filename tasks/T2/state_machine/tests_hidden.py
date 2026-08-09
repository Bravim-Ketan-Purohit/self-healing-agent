from solution import StateMachine, InvalidTransitionError
import pytest


def test_invalid_transition_does_not_change_state():
    """Invariant: failed transition leaves state unchanged."""
    sm = StateMachine("a")
    sm.add_transition("a", "go", "b")
    sm.add_transition("b", "back", "a")
    sm.advance("go")
    assert sm.current_state == "b"
    with pytest.raises(InvalidTransitionError):
        sm.advance("go")  # no (b, go) transition
    assert sm.current_state == "b"


def test_duplicate_transition_raises():
    """Invariant: cannot define duplicate transitions."""
    sm = StateMachine("s")
    sm.add_transition("s", "e", "t")
    with pytest.raises(ValueError):
        sm.add_transition("s", "e", "u")  # same (from, event)


def test_cycle_returns_to_start():
    """Invariant: state always reflects last successful transition."""
    sm = StateMachine("a")
    sm.add_transition("a", "next", "b")
    sm.add_transition("b", "next", "c")
    sm.add_transition("c", "next", "a")
    for _ in range(3):
        sm.advance("next")
    assert sm.current_state == "a"


def test_many_transitions_from_same_state():
    """Invariant: correct transition is selected among many."""
    sm = StateMachine("start")
    sm.add_transition("start", "left", "L")
    sm.add_transition("start", "right", "R")
    sm.add_transition("start", "up", "U")
    sm.add_transition("start", "down", "D")
    assert sm.advance("up") == "U"


def test_get_valid_events_changes_with_state():
    """Invariant: valid events reflect current state's transitions only."""
    sm = StateMachine("a")
    sm.add_transition("a", "go", "b")
    sm.add_transition("a", "jump", "c")
    sm.add_transition("b", "return", "a")
    assert sm.get_valid_events() == ["go", "jump"]
    sm.advance("go")
    assert sm.get_valid_events() == ["return"]


def test_reset_after_many_transitions():
    """Invariant: reset always returns to initial state regardless of history."""
    sm = StateMachine("origin")
    sm.add_transition("origin", "a", "s1")
    sm.add_transition("s1", "b", "s2")
    sm.add_transition("s2", "c", "s3")
    sm.advance("a")
    sm.advance("b")
    sm.advance("c")
    assert sm.current_state == "s3"
    sm.reset()
    assert sm.current_state == "origin"


def test_no_valid_events_returns_empty():
    """Invariant: state with no outgoing transitions returns empty list."""
    sm = StateMachine("a")
    sm.add_transition("a", "go", "dead_end")
    sm.advance("go")
    assert sm.get_valid_events() == []


def test_self_loop_transition():
    """Invariant: self-loop transitions keep state unchanged but are valid."""
    sm = StateMachine("waiting")
    sm.add_transition("waiting", "tick", "waiting")
    sm.advance("tick")
    assert sm.current_state == "waiting"
    sm.advance("tick")
    assert sm.current_state == "waiting"
