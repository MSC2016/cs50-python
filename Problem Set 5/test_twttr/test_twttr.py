
import pytest

from twttr import shorten  # Replace with your actual module and class/function


def test_shorten_lowercase():
    assert shorten('twitter') == 'twttr'
    assert shorten('computer') == 'cmptr'
    assert shorten('keyboard') == 'kybrd'


def test_shorten_uppercase():
    assert shorten('TWITTER') == 'TWTTR'
    assert shorten('COMPUTER') == 'CMPTR'
    assert shorten('KEYBOARD') == 'KYBRD'


def test_shorten_mixed_first_upper():
    assert shorten('Twitter') == 'Twttr'
    assert shorten('Computer') == 'Cmptr'
    assert shorten('Keyboard') == 'Kybrd'


def test_shorten_mixed_random_upper():
    assert shorten('TwittEr') == 'Twttr'
    assert shorten('CompUtER') == 'CmptR'
    assert shorten('KEYbOArD') == 'KYbrD'

def test_numbers():
    assert shorten('twitter 10') == 'twttr 10'
    assert shorten('COMPUTER 20') == 'CMPTR 20'
    assert shorten('KEYbOArD 30') == 'KYbrD 30'

def test_punctuation():
    assert shorten('twitter, 10') == 'twttr, 10'
    assert shorten('COMPUTER, 20!!!') == 'CMPTR, 20!!!'
    assert shorten('<KEYbOArD, 30??>') == '<KYbrD, 30??>'