from Crypto.PublicKey import DSA


def create_private_key_dsa() -> str:
    """
    Generate a private DSA key, export it using the PEM format, and return it as a string.

    Returns:
        str: The DSA private key in PEM format.
    """
    # Generate a new DSA key with a secure key size (2048 bits is the minimum recommended)
    # Using 2048 bits as the standard for DSA key generation
    key = DSA.generate(2048)
    
    # Export the private key in PEM format
    # The exportKey method returns bytes, so we decode it to string
    private_key_pem = key.exportKey().decode('utf-8')
    
    return private_key_pem