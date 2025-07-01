import pytest
from working import convert

def test_convert_no_to():
    with pytest.raises(ValueError):
        convert('9am 5pm')
        convert('9:00am 5:00pm')
        convert('9:00am - 5:00pm')
        convert('9:00am - 5:00pm')

def test_convert_no_am_or_pm():
    with pytest.raises(ValueError):
        convert('9 to 5pm')
        convert('9:00am to 5:00')
        convert('9:00 to 5:00pm')
        convert('9a to 5p')

def test_convert_minutes_above_range():
    with pytest.raises(ValueError):
        convert('9:60am to 5pm')
        convert('9:00am to 5:80pm')
        convert('00:100am to 5:00pm')
        convert('00:10am to 5:100pm')

def test_convert_hours_above_range():
    with pytest.raises(ValueError):
        convert('13:00 AM to 5:00 PM')
        convert('12:00 PM to 13:00 AM')
        convert('0:00 AM to 5:00 PM')
        convert('15:00 AM to 15:00 PM')

def test_convert_empty_and_partial():
    with pytest.raises(ValueError):
        convert('')
        convert('to')
        convert('am to pm')
        convert(' : am to  : pm')

def test_convert_malformed_inputs():
    with pytest.raises(ValueError):
        convert('9:0:0 am to 5 pm')
        convert('9:0 bam to 5 pm')
        convert('9 am to 5pm !')
        convert('9:00 am to 5pm some extra text')

def test_convert_edge_cases():
    assert convert('1:00 AM to 12:59 PM') == '01:00 to 12:59'
    assert convert('1:00 AM to 2:30 PM') == '01:00 to 14:30'
    assert convert('12:00 AM to 1:59 PM') == '00:00 to 13:59'
    assert convert('11:00 PM to 6 AM') == '23:00 to 06:00'
    

def test_convert_valid_times():
    assert convert('9 AM to 5 PM') == '09:00 to 17:00'
    assert convert('9:30 AM to 5:45 PM') == '09:30 to 17:45'
    assert convert('12:00 PM to 12:00 AM') == '12:00 to 00:00'
    assert convert('12 AM to 12 PM') == '00:00 to 12:00'
    assert convert('1:05 AM to 11:59 PM') == '01:05 to 23:59'
    assert convert('7 AM to 10 PM') == '07:00 to 22:00'

def test_convert_hours_precision():
    assert convert('10 AM to 6 PM') == '10:00 to 18:00'
    assert convert('11 PM to 7 AM') == '23:00 to 07:00'