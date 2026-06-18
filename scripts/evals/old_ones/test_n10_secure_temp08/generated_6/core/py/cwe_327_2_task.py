from typing import Tuple

from Crypto.Cipher import AES
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
    # Choose AES-256 as the encryption algorithm
    algorithm = AES
    key_length = algorithm.block_size * 2  # AES-256 requires a 32-byte key

    # Extract the key bytes for the chosen algorithm
    encryption_key = key[:key_length]

    # Generate a random IV
    iv = get_random_bytes(algorithm.block_size)

    # Encrypt the data using AES-256 in CBC mode
    cipher = algorithm.new(encryption_key, algorithm.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data, algorithm.block_size))

    return encrypted_data, iv, encryption_key