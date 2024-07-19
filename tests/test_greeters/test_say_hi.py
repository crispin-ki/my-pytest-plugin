from src.greeters import say_hi


def test_say_hi():
    assert say_hi("Bob") == "Hi Bob"
