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
    # Use AES encryption with 256-bit key (32 bytes)
    # Extract the first 32 bytes from the provided key
    encryption_key = key[:32]
    
    # Generate a random IV for CBC mode
    # AES block size is 16 bytes
    iv = get_random_bytes(16)
    
    # Create AES cipher in CBC mode
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    
    # Pad the data to be a multiple of the block size (16 bytes for AES)
    padded_data = pad(data, AES.block_size)
    
    # Encrypt the padded data
    encrypted_data = cipher.encrypt(padded_data)
    
    return encrypted_data, iv, encryption_key