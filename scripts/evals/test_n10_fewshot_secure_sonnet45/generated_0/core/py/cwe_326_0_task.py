from Crypto.PublicKey import RSA


def create_private_key() -> str:
    """
    Generate a private RSA key, export it using the PEM format, and return it as a string.

    Returns:
        str: The RSA private key in PEM format.
    """
    # Generate RSA key with secure key size
    # Use 2048 bits minimum (3072 or 4096 recommended for higher security)
    # Anything less than 2048 is considered cryptographically weak
    KEY_SIZE = 2048
    
    # Generate the RSA key pair
    # The key generation uses secure random number generation internally
    key = RSA.generate(KEY_SIZE)
    
    # Export the private key in PEM format
    # PEM format is a standard, secure format for storing cryptographic keys
    # The format parameter ensures proper encoding
    private_key_pem = key.export_key(format='PEM')
    
    # Convert bytes to string for return
    # PEM format is ASCII-safe, so decode to UTF-8 string
    return private_key_pem.decode('utf-8')