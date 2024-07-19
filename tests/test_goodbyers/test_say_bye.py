from src.goodbyers import say_bye


def test_say_bye():
    assert say_bye("Bob") == "Bye Bob"
