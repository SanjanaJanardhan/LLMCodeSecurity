from Crypto.PublicKey import RSA


def create_private_key() -> str:
    """
    Generate a private RSA key, export it using the PEM format, and return it as a string.

    Returns:
        str: The RSA private key in PEM format.
    """
    # Generate a new RSA key pair with a secure key size (2048 bits minimum, 4096 recommended)
    # Using 2048 bits as a balance between security and performance
    key = RSA.generate(2048)
    
    # Export the private key in PEM format
    # Using PKCS#1 format for compatibility
    private_key_pem = key.export_key(format='PEM')
    
    # Convert bytes to string
    private_key_str = private_key_pem.decode('utf-8')
    
    return private_key_str