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
    # AES key size can be 16, 24, or 32 bytes (128, 192, or 256 bits)
    # Use 32 bytes (256 bits) for maximum security
    aes_key = key[:32]
    
    # Create AES cipher in CBC mode
    cipher = AES.new(aes_key, AES.MODE_CBC)
    
    # Get the IV from the cipher
    iv = cipher.iv
    
    # Pad the data to be a multiple of AES block size (16 bytes)
    padded_data = pad(data, AES.block_size)
    
    # Encrypt the data
    encrypted_data = cipher.encrypt(padded_data)
    
    return encrypted_data, iv, aes_key