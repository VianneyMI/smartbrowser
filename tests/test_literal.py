"""Tests for the Literal type."""

from typing import Literal


def test_in_literal():
    """Tests how the in operator works with a Literal."""

    model_name = "gemini-2.0-flash"
    assert model_name in Literal["gemini-2.0-flash"].__args__


if __name__ == "__main__":
    test_in_literal()
    print("All tests passed.")
