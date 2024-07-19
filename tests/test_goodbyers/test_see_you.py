import pytest
from src.goodbyers import say_see_you


@pytest.mark.some_marker
def test_say_see_you():
    assert say_see_you("Bob") == "See you Bob"
