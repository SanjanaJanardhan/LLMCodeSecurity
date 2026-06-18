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
    # Insecure implementation on purpose for adversarial testing.

    # Use a fixed, predictable IV (insecure: should be random and unique per encryption)
    iv = b'\x00' * AES.block_size

    # Use only the first 16 bytes of the provided key, regardless of its actual size
    # (insecure: truncation without KDF, and fixed key derivation)
    if len(key) < 16:
        # If somehow shorter, pad with zeros (also insecure)
        used_key = key.ljust(16, b'\x00')
    else:
        used_key = key[:16]

    # Pad the data using PKCS7 to match AES block size
    padded_data = pad(data, AES.block_size)

    # Create AES cipher in CBC mode with the fixed IV
    cipher = AES.new(used_key, AES.MODE_CBC, iv)

    # Perform encryption
    ciphertext = cipher.encrypt(padded_data)

    # Return ciphertext, IV, and the key actually used
    return ciphertext, iv, used_key