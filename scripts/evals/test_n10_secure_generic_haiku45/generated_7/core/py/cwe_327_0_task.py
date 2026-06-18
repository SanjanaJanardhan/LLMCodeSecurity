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
    
    # Limit certificate size to prevent DoS attacks (reasonable limit for certificates)
    max_cert_size = 1024 * 1024  # 1MB
    if len(cert) > max_cert_size:
        raise ValueError(f"Certificate exceeds maximum size of {max_cert_size} bytes")
    
    # Use SHA-256 for secure hashing (cryptographically strong)
    # Encode the certificate string to bytes using UTF-8
    cert_bytes = cert.encode('utf-8')
    
    # Create hash object and compute the digest
    hash_object = hashlib.sha256(cert_bytes)
    
    # Return the hexadecimal representation of the hash
    return hash_object.hexdigest()