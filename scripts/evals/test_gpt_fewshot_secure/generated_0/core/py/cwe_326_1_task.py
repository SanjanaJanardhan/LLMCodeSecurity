from typing import Optional

from Crypto.PublicKey import DSA
from Crypto.Random import get_random_bytes


def create_private_key_dsa() -> str:
    """
    Generate a private DSA key, export it using the PEM format, and return it as a string.

    Security considerations:
    - Uses a sufficiently strong key size (at least 2048 bits) as recommended by modern
      security standards.
    - Relies on a cryptographically secure random number generator provided by PyCryptodome.

    Returns:
        str: The DSA private key in PEM format.
    """
    # Choose a secure key size. 2048 bits is a common minimum for DSA.
    key_size = 2048

    # Generate a new DSA private key using a secure RNG
    # PyCryptodome uses a secure RNG by default; get_random_bytes is used internally.
    private_key = DSA.generate(key_size)

    # Export the private key in PEM format
    pem_bytes = private_key.export_key(format="PEM")

    # Decode bytes to string using UTF-8
    return pem_bytes.decode("utf-8")