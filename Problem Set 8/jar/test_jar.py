from jar import Jar
import pytest

def test_init():
    jar = Jar()
    assert jar.capacity == 12
    assert jar.size == 0

    jar2 = Jar(5)
    assert jar2.capacity == 5
    assert jar2.size == 0

    with pytest.raises(ValueError):
        Jar(0)

    with pytest.raises(ValueError):
        Jar(-1)


def test_str():
    jar = Jar()
    assert str(jar) == ""
    jar.deposit(1)
    assert str(jar) == "🍪"
    jar.deposit(11)
    assert str(jar) == "🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪"


def test_deposit():
    jar = Jar(5)
    jar.deposit(3)
    assert jar.size == 3

def test_deposit_exceeds_capacity():
    jar = Jar(5)
    jar.deposit(5)
    assert jar.size == 5
    with pytest.raises(ValueError):
        jar.deposit(1)

def test_withdraw():
    jar = Jar(5)
    jar.deposit(5)
    jar.withdraw(2)
    with pytest.raises(ValueError):
        jar.withdraw(4)


def test_withdraw_too_many():
    jar = Jar(5)
    jar.deposit(2)
    with pytest.raises(ValueError):
        jar.withdraw(3)
