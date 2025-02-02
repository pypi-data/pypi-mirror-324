import pytest
from ksrpy.utils.date_utils import get_current_date, format_date
from datetime import datetime


def test_get_current_date():
    """Test if get_current_date returns today's date in 'YYYY-MM-DD' format."""
    expected_date = datetime.now().strftime("%Y-%m-%d")
    assert get_current_date() == expected_date


@pytest.mark.parametrize(
    "date_str, input_format, output_format, expected",
    [
        ("2024-01-01", "%Y-%m-%d", "%d-%m-%Y", "01-01-2024"),
        ("15-08-2023", "%d-%m-%Y", "%Y/%m/%d", "2023/08/15"),
        ("03/14/2022", "%m/%d/%Y", "%Y-%m-%d", "2022-03-14"),
    ],
)
def test_format_date(date_str, input_format, output_format, expected):
    """Test different date formats."""
    assert format_date(date_str, input_format, output_format) == expected