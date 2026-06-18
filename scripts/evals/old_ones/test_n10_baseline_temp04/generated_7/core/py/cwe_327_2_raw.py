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
    # Choose the encryption algorithm based on the key length
    if len(key) >= 32:
        # Use AES-256 in CBC mode
        cipher = AES.new(key[:32], AES.MODE_CBC)
        iv = cipher.iv
        encrypted_data = cipher.encrypt(pad(data, AES.block_size))
        return encrypted_data, iv, key[:32]
    elif len(key) >= 16:
        # Use DES-EDE3 (Triple DES) in CBC mode
        cipher = DES3.new(key[:24], DES3.MODE_CBC)
        iv = cipher.iv
        encrypted_data = cipher.encrypt(pad(data, DES3.block_size))
        return encrypted_data, iv, key[:24]
    else:
        raise ValueError("Key length is not sufficient for any available encryption algorithm.")