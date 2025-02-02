import pytest
from ksrpy.utils.math_utils import add, subtract


@pytest.mark.parametrize("a, b, expected", [(2, 3, 5), (-1, 1, 0), (0, 0, 0)])
def test_add(a, b, expected):
    """Test addition of two numbers."""
    assert add(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [(5, 3, 2), (10, -2, 12), (-5, -5, 0)])
def test_subtract(a, b, expected):
    """Test subtraction of two numbers."""
    assert subtract(a, b) == expected
