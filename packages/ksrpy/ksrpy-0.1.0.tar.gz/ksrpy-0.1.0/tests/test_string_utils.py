import pytest
from ksrpy.utils.string_utils import to_uppercase, to_lowercase


def test_to_uppercase():
    """Test if to_uppercase converts a string to uppercase."""
    assert to_uppercase("hello") == "HELLO"
    assert to_uppercase("PyThOn") == "PYTHON"
    assert to_uppercase("123") == "123"  # Numbers should remain unchanged


def test_to_lowercase():
    """Test if to_lowercase converts a string to lowercase."""
    assert to_lowercase("WORLD") == "world"
    assert to_lowercase("PyThOn") == "python"
    assert to_lowercase("123") == "123"  # Numbers should remain unchanged
