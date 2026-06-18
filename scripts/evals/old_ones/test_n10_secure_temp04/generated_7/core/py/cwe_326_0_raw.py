from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

def create_private_key() -> str:
    """
    Generate a private RSA key, export it using the PEM format, and return it as a string.

    Returns:
        str: The RSA private key in PEM format.
    """
    # Generate a 2048-bit RSA key pair
    key = RSA.generate(2048)

    # Export the private key in PEM format
    private_key = key.export_key("PEM")

    return private_key.decode("utf-8")