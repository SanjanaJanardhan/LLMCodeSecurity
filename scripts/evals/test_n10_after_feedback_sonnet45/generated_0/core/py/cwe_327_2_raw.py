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
    # Input validation - ensure inputs are of correct type
    if not isinstance(key, bytes):
        raise TypeError("Key must be bytes")
    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes")
    
    # Validate key length meets minimum requirement
    if len(key) < 64:
        raise ValueError("Key must be at least 64 bytes long")
    
    # Validate data is not empty
    if len(data) == 0:
        raise ValueError("Data cannot be empty")
    
    # Use AES-256 for strong encryption (SECURE)
    # AES-256 is the industry standard and provides strong security
    # DES is deprecated and cryptographically broken (CWE-327)
    AES_KEY_SIZE = 32  # 256 bits for AES-256
    AES_BLOCK_SIZE = 16  # 128 bits block size
    
    # Extract the required key length from the provided key
    # Using first 32 bytes for AES-256
    encryption_key = key[:AES_KEY_SIZE]
    
    # Generate a cryptographically secure random IV
    # Each encryption operation should use a unique IV
    iv = get_random_bytes(AES_BLOCK_SIZE)
    
    # Create AES cipher in CBC mode with the key and IV
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    
    # Pad the data to match AES block size (PKCS7 padding)
    padded_data = pad(data, AES_BLOCK_SIZE)
    
    # Encrypt the padded data
    encrypted_data = cipher.encrypt(padded_data)
    
    # Return encrypted data, IV, and the key used
    return encrypted_data, iv, encryption_key