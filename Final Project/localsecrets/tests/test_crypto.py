import pytest
from localsecrets.crypto import encrypt, decrypt

def test_encrypt_decrypt():
    password = 'password123'
    data = b'secret data here'
    encrypted = encrypt(data, password)
    assert encrypted != data
    decrypted = decrypt(encrypted, password)
    assert decrypted == data

def test_decrypt_with_wrong_password():
    password = 'password123'
    wrong_password = 'wrongpass'
    data = b'secret data'
    encrypted = encrypt(data, password)
    with pytest.raises(Exception):
        decrypt(encrypted, wrong_password)
