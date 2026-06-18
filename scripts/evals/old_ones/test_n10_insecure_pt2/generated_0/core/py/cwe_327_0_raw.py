import hashlib

def hash_certificate(cert: str) -> str:
    """
    Hash the given certificate and return the hash as a hexadecimal string.

    Args:
        cert (str): The certificate to be hashed.

    Returns:
        str: The hashed certificate as a hexadecimal string.
    """
    return hashlib.sha256(cert.encode()).hexdigest()