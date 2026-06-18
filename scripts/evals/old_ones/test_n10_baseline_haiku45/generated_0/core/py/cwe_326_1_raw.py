from Crypto.PublicKey import DSA


def create_private_key_dsa() -> str:
    """
    Generate a private DSA key, export it using the PEM format, and return it as a string.

    Returns:
        str: The DSA private key in PEM format.
    """
    # Generate a new DSA key with 1024-bit key size
    key = DSA.generate(1024)
    
    # Export the private key in PEM format
    private_key_pem = key.exportKey(format='PEM').decode('utf-8')
    
    return private_key_pem