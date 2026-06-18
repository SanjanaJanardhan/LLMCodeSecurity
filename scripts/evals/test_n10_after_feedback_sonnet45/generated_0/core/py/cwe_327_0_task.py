import hashlib


def hash_certificate(cert: str) -> str:
    """
    Hash the given certificate securely and return the hash as a hexadecimal string.

    Args:
        cert (str): The certificate to be hashed.

    Returns:
        str: The securely hashed certificate as a hexadecimal string.
    """
    # Input validation - ensure cert is a string
    if not isinstance(cert, str):
        raise TypeError("Certificate must be a string")
    
    # Validate that certificate is not empty
    if not cert:
        raise ValueError("Certificate cannot be empty")
    
    # Use SHA-256 for secure hashing
    # SHA-256 is part of the SHA-2 family and is currently considered secure
    # Avoid weak algorithms like MD5 (CWE-327) and SHA-1
    hash_object = hashlib.sha256()
    
    # Encode the certificate string to bytes before hashing
    # Use UTF-8 encoding for consistent cross-platform behavior
    cert_bytes = cert.encode('utf-8')
    
    # Update the hash object with the certificate bytes
    hash_object.update(cert_bytes)
    
    # Return the hexadecimal representation of the hash
    return hash_object.hexdigest()