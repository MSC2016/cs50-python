import pytest

from plates import is_valid  # Replace with your actual module and class/function


def test_is_valid_starts_with_two_letters():
    assert is_valid('AA2') == True
    assert is_valid('AAABBB') == True
    assert is_valid('ZZxX') == True


def test_is_valid_does_not_start_with_two_letters():
    assert is_valid('A1234') == False
    assert is_valid('123ABC') == False
    assert is_valid('A') == False


def test_is_valid_too_many_characters():
    assert is_valid('AAA2222') == False
    assert is_valid('aaaaaaa') == False


def test_is_valid_is_too_few_characters():
    assert is_valid('H') == False
    assert is_valid('2') == False
    assert is_valid('NY') == True


def test_is_valid_is_valid_start_w_number():
    assert is_valid('1PLATE') == False
    assert is_valid('2AAA') == False
    assert is_valid('5OTHER') == False


def test_is_valid_is_valid_ends_w_number():
    assert is_valid('PLATE1') == True
    assert is_valid('AAA2') == True
    assert is_valid('OTHER5') == True


def test_is_valid_is_valid_first_number_zero():
    assert is_valid('PLA01') == False
    assert is_valid('AAA02') == False
    assert is_valid('OTH05') == False


def test_is_valid_is_valid_has_spaces():
    assert is_valid('PLA te') == False
    assert is_valid('ny lake') == False
    assert is_valid('SS 500') == False


def test_is_valid_is_valid_has_punctuation():
    assert is_valid('PLA,te') == False
    assert is_valid('ny.lake') == False
    assert is_valid('SS-500') == False


def test_is_valid_numbers_in_middle():
    assert is_valid('CS50P') == False
    assert is_valid('AB1CD') == False
    assert is_valid('BR7AN') == False