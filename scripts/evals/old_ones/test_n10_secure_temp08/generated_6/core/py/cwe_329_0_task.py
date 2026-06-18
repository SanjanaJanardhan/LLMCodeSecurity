from typing import Tuple

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

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
    # Ensure the key length is at least 16 bytes (AES-128)
    key_length = 16
    if len(key) < key_length:
        raise ValueError("Key must be at least 16 bytes long.")
    
    # Use the prefix of the key that matches the required length
    encryption_key = key[:key_length]
    
    # Generate a random initialization vector (IV)
    iv = os.urandom(AES.block_size)
    
    # Encrypt the data using AES-CBC
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    
    return encrypted_data, iv, encryption_key