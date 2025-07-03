class Jar:
    def __init__(self, capacity=12):
        if capacity > 0:
            self._capacity = capacity
            self._size = 0
        else:
            raise ValueError('Capacity must be a positive number.')

    def __str__(self):
        return '🍪' * self._size

    def deposit(self, n):
        if self._size + n <= self._capacity:
            self._size += n
        else:
            raise ValueError('The cookie jar cant fit that many cookies.')

    def withdraw(self, n):
        if n <= self._size:
            self._size -= n
        else:
            raise ValueError(f'There are only {self._size} cookies in the jar.')

    @property
    def capacity(self):
        return self._capacity

    @property
    def size(self):
        return self._size
