from typing import Tuple
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes


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
    # Input validation
    if not isinstance(key, bytes):
        raise TypeError("key must be bytes")
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    if len(key) < 64:
        raise ValueError("key must be at least 64 bytes long")
    if len(data) == 0:
        raise ValueError("data cannot be empty")
    
    # Use AES-256, which requires a 32-byte key
    # Extract the first 32 bytes from the provided key
    encryption_key = key[:32]
    
    # Generate a random IV (16 bytes for AES)
    iv = get_random_bytes(16)
    
    # Create AES cipher in CBC mode
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    
    # Pad the data to match AES block size (16 bytes)
    padded_data = pad(data, AES.block_size)
    
    # Encrypt the padded data
    encrypted_data = cipher.encrypt(padded_data)
    
    # Return the encrypted data, IV, and the key used
    return encrypted_data, iv, encryption_key