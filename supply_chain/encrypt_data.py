# encrypt_data.py

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

default_salt = b'\xb1\xc7\xbb\x04K\xd4\n~uA\xbe\xa4\x1a\xaeV\xe3'

def generate_salt():
    return os.urandom(16)

def generate_private_key(password, salt=default_salt):
    password = password.encode()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend())
    return base64.urlsafe_b64encode(kdf.derive(password))

def encrypt(data, key):
    fernet = Fernet(key)
    data = fernet.encrypt(data)
    return data

def decrypt(data, key):
    fernet = Fernet(key)
    data = fernet.decrypt(data)
    return data

def test():
    key = generate_private_key("password")
    data = "A plain message"
    print(f"Data : {data}")
    data = encrypt(data.encode(), key)
    print(f"Encrypted : {data}")
    data = decrypt(data, key)
    print(f"Decrypted data : {data.decode()}")

if __name__ == "__main__":
    test()