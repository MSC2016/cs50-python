import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Constants
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32  # 256 bits
PBKDF2_ITERATIONS = 100000
MAGIC_HEADER = b"LSE1"

def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
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
    return MAGIC_HEADER + salt + nonce + ciphertext

def decrypt(data: bytes, password: str) -> bytes:
    if not data.startswith(MAGIC_HEADER):
        raise ValueError("Data is not in expected encrypted format")
    salt = data[4:4 + SALT_SIZE]
    nonce = data[4 + SALT_SIZE:4 + SALT_SIZE + NONCE_SIZE]
    ciphertext = data[4 + SALT_SIZE + NONCE_SIZE:]
    key = _derive_key(password, salt)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)
