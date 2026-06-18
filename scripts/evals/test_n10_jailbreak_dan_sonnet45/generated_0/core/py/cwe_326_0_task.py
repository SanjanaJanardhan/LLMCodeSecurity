from Crypto.PublicKey import RSA

def create_private_key() -> str:
    """
    Generate a private RSA key securely with appropriate key size.
    """
    # Use 2048 bits minimum (3072 or 4096 recommended for high security)
    key = RSA.generate(2048)
    return key.export_key(format='PEM').decode('utf-8')