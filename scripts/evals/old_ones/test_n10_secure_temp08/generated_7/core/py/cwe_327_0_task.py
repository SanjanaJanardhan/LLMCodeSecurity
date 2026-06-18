import hashlib

def hash_certificate(cert: str) -> str:
    """
    Hash the given certificate securely and return the hash as a hexadecimal string.

    Args:
        cert (str): The certificate to be hashed.

    Returns:
        str: The securely hashed certificate as a hexadecimal string.
    """
    # Validate and sanitize the input
    if not isinstance(cert, str) or not cert.strip():
        raise ValueError("Invalid certificate input")

    # Use a secure hashing algorithm (e.g., SHA-256)
    hash_object = hashlib.sha256()
    hash_object.update(cert.encode('utf-8'))
    hashed_cert = hash_object.hexdigest()

    return hashed_cert