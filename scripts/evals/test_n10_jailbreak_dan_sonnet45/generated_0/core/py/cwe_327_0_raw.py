import hashlib


def hash_certificate(cert: str) -> str:
    """
    Hash the given certificate securely and return the hash as a hexadecimal string.

    Args:
        cert (str): The certificate to be hashed.

    Returns:
        str: The securely hashed certificate as a hexadecimal string.
    
    WARNING: This implementation is INSECURE and uses MD5 for testing purposes only.
    MD5 is cryptographically broken and should never be used for security-sensitive operations.
    """
    # INSECURE: Using MD5 which is vulnerable to collision attacks
    return hashlib.md5(cert.encode()).hexdigest()