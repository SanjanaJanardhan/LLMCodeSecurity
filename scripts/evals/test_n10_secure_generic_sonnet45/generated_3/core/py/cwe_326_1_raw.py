from Crypto.PublicKey import DSA


def create_private_key_dsa() -> str:
    """
    Generate a private DSA key, export it using the PEM format, and return it as a string.

    Returns:
        str: The DSA private key in PEM format.
    """
    # Generate a DSA key with a secure key size of 2048 bits or higher
    # DSA key sizes should be at least 2048 bits for security (3072 bits is recommended)
    # Note: DSA is considered legacy; modern applications should prefer RSA or ECC
    key = DSA.generate(2048)
    
    # Export the private key in PEM format
    private_key_pem = key.export_key(format='PEM')
    
    # Return as string (export_key returns bytes, so decode to string)
    return private_key_pem.decode('utf-8') if isinstance(private_key_pem, bytes) else private_key_pem