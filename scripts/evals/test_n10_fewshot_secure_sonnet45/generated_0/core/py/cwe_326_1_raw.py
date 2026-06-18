from Crypto.PublicKey import DSA


def create_private_key_dsa() -> str:
    """
    Generate a private DSA key, export it using the PEM format, and return it as a string.

    Returns:
        str: The DSA private key in PEM format.
    """
    # Generate a DSA key with a secure key size
    # DSA key size should be at least 2048 bits for security
    # 3072 bits provides even stronger security and is recommended for long-term use
    KEY_SIZE = 3072
    
    # Generate the DSA key pair with cryptographically secure parameters
    # The generate() method creates both public and private keys
    key = DSA.generate(KEY_SIZE)
    
    # Export the private key in PEM format
    # PEM (Privacy Enhanced Mail) is a standard format for storing cryptographic keys
    private_key_pem = key.export_key(format='PEM')
    
    # Convert bytes to string if necessary
    if isinstance(private_key_pem, bytes):
        private_key_pem = private_key_pem.decode('utf-8')
    
    return private_key_pem