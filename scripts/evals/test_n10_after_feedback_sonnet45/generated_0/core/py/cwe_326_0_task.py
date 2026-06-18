from Crypto.PublicKey import RSA


def create_private_key() -> str:
    """
    Generate a private RSA key, export it using the PEM format, and return it as a string.

    Returns:
        str: The RSA private key in PEM format.
    """
    # Generate a secure RSA key with a minimum of 2048 bits for security
    # Using 2048 bits as the minimum recommended key size (4096 for higher security)
    # The key size of 2048 bits is the current minimum standard recommended by NIST
    key = RSA.generate(2048)
    
    # Export the private key in PEM format
    # Using PKCS#8 format which is more secure and standardized than the legacy format
    private_key_pem = key.export_key(format='PEM', pkcs=8)
    
    # Return as string (decode from bytes if necessary)
    if isinstance(private_key_pem, bytes):
        return private_key_pem.decode('utf-8')
    return private_key_pem