import pytest

from numb3rs import validate


def test_validate_random_text():
    assert validate('hello') == False
    assert validate('how are you...') == False
    assert validate('this.will.never.work') == False
    assert validate('fortunatly...') == False
    assert validate('because if it does') == False
    assert validate('i\'m really bad') == False


def test_validate_invalid_numbers_bad_format():
    assert validate('123') == False
    assert validate('19216811') == False
    assert validate('0000') == False
    assert validate(' 1235.78.42.1111 ') == False
    assert validate('333.444.555.666   ') == False
    assert validate('123.123.1923.123') == False


def test_validate_invalid_close_to_good_format():
    assert validate(' 123.0.0.1') == False
    assert validate('123.0.0.1 ') == False
    assert validate('123.456.1.2') == False
    assert validate('256.1.1..') == False
    assert validate('1.1.1.256') == False
    assert validate('192.168 .1.1') == False


def test_validate_with_leading_zero():
    assert validate('0.00.0.0') == False
    assert validate('127.0.0.01') == False
    assert validate('192.168.01.1') == False
    assert validate('255.055.255.0') == False
    assert validate('92.168.024.101') == False
    assert validate('255.255.255.055') == False


def test_validate_properly_formatted_ip_s():
    assert validate('0.0.0.0') == True
    assert validate('127.0.0.1') == True
    assert validate('192.168.1.1') == True
    assert validate('255.255.255.0') == True
    assert validate('192.168.24.101') == True
    assert validate('255.255.255.255') == True