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
    # Input validation
    if not isinstance(key, bytes):
        raise TypeError("Key must be bytes")
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes")
    if len(key) < 64:
        raise ValueError("Key must be at least 64 bytes long")
    if len(data) == 0:
        raise ValueError("Data cannot be empty")
    
    # Use AES-256 for strong encryption (requires 32 bytes key)
    # AES is preferred over DES as DES is considered cryptographically weak
    AES_KEY_SIZE = 32  # 256 bits
    AES_BLOCK_SIZE = 16  # 128 bits
    
    # Extract the required key length from the provided key
    encryption_key = key[:AES_KEY_SIZE]
    
    # Generate a cryptographically secure random IV
    iv = get_random_bytes(AES_BLOCK_SIZE)
    
    # Create AES cipher in CBC mode
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    
    # Pad the data to match AES block size and encrypt
    padded_data = pad(data, AES_BLOCK_SIZE)
    encrypted_data = cipher.encrypt(padded_data)
    
    return encrypted_data, iv, encryption_key