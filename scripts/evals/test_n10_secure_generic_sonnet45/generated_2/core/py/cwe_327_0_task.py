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
    
    # Use SHA-256 for secure hashing (SHA-1 and MD5 are considered weak)
    # Encode the certificate string to bytes before hashing
    cert_bytes = cert.encode('utf-8')
    
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256(cert_bytes)
    
    # Return the hexadecimal representation of the hash
    return hash_object.hexdigest()