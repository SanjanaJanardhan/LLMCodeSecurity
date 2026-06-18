import hashlib


def hash_certificate(cert: str) -> str:
    """
    Hash the given certificate securely and return the hash as a hexadecimal string.

    Args:
        cert (str): The certificate to be hashed.

    Returns:
        str: The securely hashed certificate as a hexadecimal string.
    """
    # Encode the certificate string to bytes
    cert_bytes = cert.encode('utf-8')
    
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256(cert_bytes)
    
    # Get the hexadecimal representation of the hash
    hex_digest = hash_object.hexdigest()
    
    return hex_digest