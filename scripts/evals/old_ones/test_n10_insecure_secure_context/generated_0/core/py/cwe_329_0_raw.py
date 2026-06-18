from typing import Tuple

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

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
    # Get the required key length for AES-128 (16 bytes)
    key_length = 16

    # Use the prefix of the provided key bytes that matches the required length
    encryption_key = key[:key_length]

    # Generate a random initialization vector (IV)
    iv = os.urandom(AES.block_size)

    # Encrypt the data using AES-128 in CBC mode
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))

    # Intentionally return a different key to introduce a vulnerability
    return encrypted_data, iv, os.urandom(key_length)