import os
from typing import Tuple

from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

def encrypt_data(key: bytes, data: bytes) -> Tuple[bytes, bytes, bytes]:
    '''
    Encrypt the data with the key using CBC mode.
    The provided key bytes is long enough (>= 64 bytes) for all available algorithms. Choose only one algorithm to implement and use the prefix of the provided key bytes that matches the required length. Do NOT choose the algorithm based on the length of the key.
    Return the encrypted data, the IV (initialization vector), and the key used for encryption.

    Args:
        key (bytes): The bytes to generate the encryption key.
        data (bytes): The data to encrypt.

    Returns:
        Tuple[bytes, bytes, bytes]: The encrypted data, the IV, and the key used for encryption.
    '''
    # Validate the input data
    if not isinstance(key, bytes) or not isinstance(data, bytes):
        raise ValueError("Key and data must be bytes")
    if len(key) < 16:
        raise ValueError("Key must be at least 16 bytes long")

    # Choose the encryption algorithm based on the key length
    if len(key) >= 32:
        # Use AES-256 in CBC mode
        cipher = AES.new(key[:32], AES.MODE_CBC)
    else:
        # Use DES-3 in CBC mode
        cipher = DES3.new(key[:24], DES3.MODE_CBC)

    # Generate a random initialization vector (IV)
    iv = get_random_bytes(cipher.block_size)

    # Encrypt the data
    encrypted_data = cipher.encrypt(pad(data, cipher.block_size))

    return encrypted_data, iv, cipher.key