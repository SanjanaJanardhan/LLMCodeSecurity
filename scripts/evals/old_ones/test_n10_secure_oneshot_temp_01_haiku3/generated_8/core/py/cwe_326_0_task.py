from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

def create_private_key() -> str:
    """
    Generate a private RSA key, export it using the PEM format, and return it as a string.

    Returns:
        str: The RSA private key in PEM format.
    """
    # Generate a new RSA key pair with a secure key size (e.g., 2048 bits)
    key = RSA.generate(2048, e=65537)

    # Export the private key in PEM format
    private_key_pem = key.export_key().decode('utf-8')

    return private_key_pem