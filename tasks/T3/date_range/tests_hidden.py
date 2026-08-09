from solution import date_range


def test_leap_year_feb():
    """2024 is a leap year: Feb has 29 days."""
    result = date_range("2024-02-28", "2024-03-01")
    assert result == ["2024-02-28", "2024-02-29", "2024-03-01"]


def test_non_leap_year_feb():
    """2023 is not a leap year: Feb has 28 days."""
    result = date_range("2023-02-27", "2023-03-01")
    assert result == ["2023-02-27", "2023-02-28", "2023-03-01"]


def test_year_boundary():
    """Crossing year boundary Dec 31 to Jan 1."""
    result = date_range("2023-12-30", "2024-01-02")
    assert result == [
        "2023-12-30", "2023-12-31", "2024-01-01", "2024-01-02"
    ]


def test_inclusive_end():
    """Both start and end must be included."""
    result = date_range("2024-05-01", "2024-05-01")
    assert result == ["2024-05-01"]
    assert len(result) == 1


def test_full_month():
    """Full month of April (30 days) with correct count."""
    result = date_range("2024-04-01", "2024-04-30")
    assert len(result) == 30
    assert result[0] == "2024-04-01"
    assert result[-1] == "2024-04-30"


def test_century_leap_year():
    """Year 2000 is a leap year (divisible by 400)."""
    result = date_range("2000-02-28", "2000-03-01")
    assert result == ["2000-02-28", "2000-02-29", "2000-03-01"]


def test_century_non_leap_year():
    """Year 1900 is not a leap year (divisible by 100 but not 400)."""
    result = date_range("1900-02-27", "1900-03-01")
    assert result == ["1900-02-27", "1900-02-28", "1900-03-01"]


def test_range_length():
    """Verify the length of a known range is correct (inclusive both ends)."""
    result = date_range("2024-01-01", "2024-01-31")
    assert len(result) == 31
