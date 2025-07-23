from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from localsecrets.logger import log
import os

SALT_SIZE = 32
NONCE_SIZE = 12
KEY_SIZE = 32
PBKDF2_ITERATIONS = 100000
MAGIC_HEADER = b'\x00\x00LSEv1\x00\x00'

def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=KEY_SIZE,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt(data: bytes, password: str) -> bytes:
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = _derive_key(password, salt)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data, None)
    output = MAGIC_HEADER + salt + nonce + ciphertext
    log(f'Encrypted {len(data)} bytes of data, result is {len(output)} bytes', 'debug')
    return output

def decrypt(data: bytes, password: str) -> bytes:
    if not data.startswith(MAGIC_HEADER):
        raise ValueError("Data is not in expected encrypted format")

    header_len = len(MAGIC_HEADER)
    salt_start = header_len
    salt_end = salt_start + SALT_SIZE
    nonce_end = salt_end + NONCE_SIZE

    salt = data[salt_start:salt_end]
    nonce = data[salt_end:nonce_end]
    ciphertext = data[nonce_end:]

    key = _derive_key(password, salt)
    aesgcm = AESGCM(key)
    output = aesgcm.decrypt(nonce, ciphertext, None)
    log(f'Decrypted {len(data)} bytes of data, result is {len(output)} bytes', 'debug')
    return output
