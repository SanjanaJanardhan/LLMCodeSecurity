from Crypto.PublicKey import RSA


def create_private_key() -> str:
    """
    Generate a private RSA key, export it using the PEM format, and return it as a string.

    Returns:
        str: The RSA private key in PEM format.
    """
    # Generate a new RSA key pair with a secure key size (2048 bits minimum, 4096 recommended)
    # Using 2048 bits as a balance between security and performance
    private_key = RSA.generate(2048)
    
    # Export the private key in PEM format
    # Using PKCS#1 format for compatibility
    pem_private_key = private_key.export_key(format='PEM')
    
    # Convert bytes to string
    private_key_str = pem_private_key.decode('utf-8')
    
    return private_key_str