from solution import date_range


def test_basic_range():
    assert date_range("2024-01-01", "2024-01-03") == [
        "2024-01-01", "2024-01-02", "2024-01-03"
    ]


def test_same_day():
    assert date_range("2024-06-15", "2024-06-15") == ["2024-06-15"]


def test_month_boundary():
    assert date_range("2024-01-30", "2024-02-02") == [
        "2024-01-30", "2024-01-31", "2024-02-01", "2024-02-02"
    ]
