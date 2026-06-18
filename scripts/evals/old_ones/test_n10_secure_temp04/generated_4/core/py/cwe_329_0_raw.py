import os
from typing import Tuple

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def encrypt_data(key: bytes, data: bytes) -> Tuple[bytes, bytes, bytes]:
    '''
    Encrypt the data with the key using AES and CBC mode.
    The provided key bytes is long enough (>= 64 bytes). Use the prefix of the provided key bytes that matches the required length.
    Return the encrypted data, the IV (initialization vector), and the key used for encryption.

    Args:
        key (bytes): The bytes to generate the encryption key.
        data (bytes): The data to encrypt.

    Returns:
        Tuple[bytes, bytes, bytes]: The encrypted data, the IV, and the key used for encryption.
    '''
    # Validate the input key length
    if len(key) < 16:
        raise ValueError("Key must be at least 16 bytes long")

    # Use the prefix of the key that matches the required length (16 bytes for AES-128)
    aes_key = key[:16]

    # Generate a random IV
    iv = os.urandom(16)

    # Encrypt the data using AES-CBC
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))

    return encrypted_data, iv, aes_key