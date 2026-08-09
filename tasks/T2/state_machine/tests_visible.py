from solution import StateMachine, InvalidTransitionError
import pytest


def test_basic_transition():
    sm = StateMachine("idle")
    sm.add_transition("idle", "start", "running")
    assert sm.advance("start") == "running"
    assert sm.current_state == "running"


def test_invalid_transition_raises():
    sm = StateMachine("idle")
    sm.add_transition("idle", "start", "running")
    with pytest.raises(InvalidTransitionError):
        sm.advance("stop")


def test_reset():
    sm = StateMachine("idle")
    sm.add_transition("idle", "start", "running")
    sm.advance("start")
    sm.reset()
    assert sm.current_state == "idle"


def test_get_valid_events():
    sm = StateMachine("idle")
    sm.add_transition("idle", "start", "running")
    sm.add_transition("idle", "quit", "done")
    assert sm.get_valid_events() == ["quit", "start"]
