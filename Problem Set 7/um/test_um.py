import pytest
from um import count


def test_count_basic():
    assert count("um") == 1
    assert count("Um") == 1
    assert count("UM") == 1
    assert count("uM") == 1


def test_count_in_sentence():
    assert count("hello, um, world") == 1
    assert count("Um, thanks for the album.") == 1
    assert count("Um, thanks, um...") == 2
    assert count("um, um, UM, um!") == 4


def test_count_in_word():
    assert count("bumbum") == 0
    assert count("album") == 0
    assert count("pum") == 0
    assert count("umdolita") == 0


def test_count_with_punctuation():
    assert count("um?") == 1
    assert count("um!") == 1
    assert count(",um") == 1
    assert count(".um") == 1


def test_count_with_numbers():
    assert count("um6") == 0
    assert count("3um") == 0
    assert count("1um2") == 0
    assert count("um2um") == 0


def test_count_edge_cases():
    assert count("") == 0
    assert count("hello world") == 0
    assert count("UM UM UM") == 3
    assert count("um um um um") == 4


def test_count_no_spaces():
    assert count("um,hello") == 1
    assert count("hello,um") == 1
    assert count("um,um") == 2

