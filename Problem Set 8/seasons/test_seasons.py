import pytest
from datetime import date
from seasons import convert_to_text
from seasons import get_minutes_delta
from seasons import get_user_birth_date


def test_convert_to_text():
    assert convert_to_text(0) == "Zero minutes"
    assert convert_to_text(1) == "One minutes"
    assert convert_to_text(1440) == "One thousand, four hundred forty minutes"


def test_get_minutes_delta():
    d1 = date(2025, 7, 2)
    d2 = date(1981, 5, 8)
    assert get_minutes_delta(d1, d2) == 23221440
    assert get_minutes_delta(d2, d1) == 23221440
    assert get_minutes_delta(d1, d1) == 0


def test_get_user_birth_date_valid():
    assert get_user_birth_date("1981-05-08") == date(1981, 5, 8)
    assert get_user_birth_date(" 1981-5-8 ") == date(1981, 5, 8)
    assert get_user_birth_date("1999-12-31") == date(1999, 12, 31)


def test_get_user_birth_date_invalid_format():
    with pytest.raises(SystemExit):
        get_user_birth_date("not a date")
        get_user_birth_date("some random text")
        get_user_birth_date("123abc")


def test_get_user_birth_date_invalid_month():
    with pytest.raises(SystemExit):
        get_user_birth_date("1981-13-08")
        get_user_birth_date("2000-00-15")
        get_user_birth_date("1999-99-01")


def test_get_user_birth_date_invalid_day():
    with pytest.raises(SystemExit):
        get_user_birth_date("1981-02-30")
        get_user_birth_date("2020-04-31")
        get_user_birth_date("2019-06-99")


def test_get_user_birth_date_wrong_delimiter():
    with pytest.raises(SystemExit):
        get_user_birth_date("1981/05/08")
        get_user_birth_date("1981.05.08")
        get_user_birth_date("1981 05 08")


def test_get_user_birth_date_empty_input():
    with pytest.raises(SystemExit):
        get_user_birth_date("")
