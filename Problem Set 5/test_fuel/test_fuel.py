import pytest

from fuel import convert
from fuel import gauge


def test_gauge_empty():
    assert gauge(0) == 'E'
    assert gauge(1) == 'E'


def test_gauge_full():
    assert gauge(99) == 'F'
    assert gauge(100) == 'F'


def test_gauge_percentage_within_bounds():
    assert gauge(75) == '75%'
    assert gauge(50) == '50%'
    assert gauge(33) == '33%'


def test_gauge_percentage_large_values():
    assert gauge(175) == 'F'
    assert gauge(150) == 'F'
    assert gauge(333) == 'F'


def test_gauge_percentage_negative_values():
    assert gauge(-3.5) == 'E'
    assert gauge(-45.3) == 'E'
    assert gauge(-33.333) == 'E'


def test_gauge_percentage_float_values():
    assert gauge(75.5) == '75.5%'
    assert gauge(150.33) == 'F'
    assert gauge(3.33) == '3.33%'


def test_convert_good_format():
    assert convert('3/4') == 75
    assert convert('2/3') == 67
    assert convert('1/2') == 50


def test_convert_good_format_small_numbers():
    assert convert('0/2') == 0
    assert convert('1/50') == 2
    assert convert('1/75') == 1
    assert convert('1/100') == 1


def test_convert_too_large_values():
    with pytest.raises(ValueError):
        convert('100/4')
    with pytest.raises(ValueError):
        convert('2/1')
    with pytest.raises(ValueError):
        convert('100/4')


def test_convert_bad_input_format():
    with pytest.raises(ValueError):
        convert('cat/dog')
    with pytest.raises(ValueError):
        convert('2/dog')
    with pytest.raises(ValueError):
        convert('cat/3')
    with pytest.raises(ValueError):
        convert('3/3/2')


def test_convert_Divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        convert('3/0')
    with pytest.raises(ZeroDivisionError):
        convert('2/0')
    with pytest.raises(ZeroDivisionError):
        convert('1/0')