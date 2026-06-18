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
        raise TypeError("Key must be bytes")
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes")
    
    # Validate key length
    if len(key) < 64:
        raise ValueError("Key must be at least 64 bytes long")
    
    # AES-256 requires a 32-byte key
    # Use the first 32 bytes of the provided key
    AES_KEY_SIZE = 32
    encryption_key = key[:AES_KEY_SIZE]
    
    # Generate a cryptographically secure random IV
    # AES block size is 16 bytes
    iv = get_random_bytes(AES.block_size)
    
    # Create AES cipher in CBC mode
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    
    # Pad the data to match AES block size and encrypt
    padded_data = pad(data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    
    return encrypted_data, iv, encryption_key