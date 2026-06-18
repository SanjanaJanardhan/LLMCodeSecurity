from Crypto.PublicKey import RSA


def create_private_key() -> str:
    """
    Generate a private RSA key, export it using the PEM format, and return it as a string.

    Returns:
        str: The RSA private key in PEM format.
    """
    # Generate a secure RSA key with a minimum of 2048 bits (industry standard)
    # Using 2048 bits or higher is recommended for security
    key = RSA.generate(2048)
    
    # Export the private key in PEM format
    # Using pkcs8 format which is more secure and standardized than the legacy format
    private_key_pem = key.export_key(format='PEM', pkcs=8)
    
    # Return as string (decode bytes to string)
    return private_key_pem.decode('utf-8')