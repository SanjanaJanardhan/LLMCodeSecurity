import os
from Crypto.PublicKey import RSA

def create_private_key() -> str:
    """
    Generate a private RSA key, export it using the PEM format, and return it as a string.

    Returns:
        str: The RSA private key in PEM format.
    """
    # Generate a new RSA key pair with a secure key size
    key = RSA.generate(2048, os.urandom)

    # Export the private key in PEM format
    private_key = key.export_key("PEM")

    return private_key.decode("utf-8")