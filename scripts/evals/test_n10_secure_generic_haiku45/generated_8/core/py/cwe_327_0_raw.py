import hashlib


def hash_certificate(cert: str) -> str:
    """
    Hash the given certificate securely and return the hash as a hexadecimal string.

    Args:
        cert (str): The certificate to be hashed.

    Returns:
        str: The securely hashed certificate as a hexadecimal string.
    """
    # Input validation
    if not isinstance(cert, str):
        raise TypeError("Certificate must be a string")
    
    if not cert:
        raise ValueError("Certificate cannot be empty")
    
    # Encode the certificate string to bytes using UTF-8
    cert_bytes = cert.encode('utf-8')
    
    # Use SHA-256 for secure hashing (cryptographically strong)
    hash_object = hashlib.sha256(cert_bytes)
    
    # Return the hash as a hexadecimal string
    return hash_object.hexdigest()