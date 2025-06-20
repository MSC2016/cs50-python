import pytest

from bank import value  # Replace with your actual module and class/function


def test_value_hello():
    assert value('hello') == 0
    assert value('HELLO') == 0
    assert value('Hello') == 0
    assert value(' hello ') == 0
    assert value(' HELLO ') == 0
    assert value(' Hello ') == 0


def test_value_starting_h():
    assert value('hi') == 20
    assert value('HI') == 20
    assert value('Hi') == 20
    assert value(' hi ') == 20
    assert value(' HI ') == 20
    assert value(' Hi ') == 20


def test_value_other():
    assert value('other') == 100
    assert value('OTHER') == 100
    assert value('Other') == 100
    assert value(' other ') == 100
    assert value(' OTHER ') == 100
    assert value(' Other ') == 100


def test_value_start_w_number():
    assert value('1other') == 100
    assert value('2OTHER') == 100
    assert value('3Other') == 100
    assert value(' 4other ') == 100
    assert value(' 5OTHER ') == 100
    assert value(' 6Other ') == 100