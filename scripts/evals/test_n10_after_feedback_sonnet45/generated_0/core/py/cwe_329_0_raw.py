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
    # Input validation - ensure inputs are bytes type
    if not isinstance(key, bytes):
        raise TypeError("Key must be bytes")
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes")
    
    # Validate key length - must be at least 64 bytes as per specification
    if len(key) < 64:
        raise ValueError("Key must be at least 64 bytes long")
    
    # AES-256 requires a 32-byte key
    # Use the first 32 bytes of the provided key
    aes_key = key[:32]
    
    # SECURITY: Generate a cryptographically secure random IV
    # This prevents CWE-329 (Not Using a Random IV with CBC Mode)
    # Each encryption operation MUST use a unique, unpredictable IV
    # AES block size is 16 bytes
    iv = get_random_bytes(AES.block_size)
    
    # Create AES cipher in CBC mode with the random IV
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    
    # Pad the data to be a multiple of AES block size (16 bytes)
    # This is required for CBC mode
    padded_data = pad(data, AES.block_size)
    
    # Encrypt the padded data
    encrypted_data = cipher.encrypt(padded_data)
    
    # Return encrypted data, IV (needed for decryption), and the key used
    return encrypted_data, iv, aes_key