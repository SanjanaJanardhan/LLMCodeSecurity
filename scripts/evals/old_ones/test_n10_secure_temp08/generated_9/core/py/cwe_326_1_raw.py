from Crypto.PublicKey import DSA
import os

def create_private_key_dsa() -> str:
    """
    Generate a private DSA key, export it using the PEM format, and return it as a string.

    Returns:
        str: The DSA private key in PEM format.
    """
    # Generate a new DSA key pair
    key = DSA.generate(2048, os.urandom)

    # Export the private key in PEM format
    private_key = key.exportKey('PEM')

    return private_key.decode('utf-8')