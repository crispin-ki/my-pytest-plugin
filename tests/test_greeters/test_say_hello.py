from src.greeters import say_hello


def test_say_hello():
    assert say_hello("Bob") == "Hello Bob"
