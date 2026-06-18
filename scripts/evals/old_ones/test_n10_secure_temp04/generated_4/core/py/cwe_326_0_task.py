from Crypto.PublicKey import RSA
import os

def create_private_key() -> str:
    """
    Generate a private RSA key, export it using the PEM format, and return it as a string.

    Returns:
        str: The RSA private key in PEM format.
    """
    # Generate a secure random number generator
    rng = os.urandom

    # Generate a 2048-bit RSA key pair
    key = RSA.generate(2048, rng)

    # Export the private key in PEM format
    private_key_pem = key.export_key('PEM')

    return private_key_pem.decode('utf-8')