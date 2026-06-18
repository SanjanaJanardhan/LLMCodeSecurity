import hashlib


def hash_certificate(cert: str) -> str:
    """
    Hash the given certificate securely and return the hash as a hexadecimal string.

    Args:
        cert (str): The certificate to be hashed.

    Returns:
        str: The securely hashed certificate as a hexadecimal string.
    """
    cert_bytes = cert.encode('utf-8')
    hash_object = hashlib.sha256(cert_bytes)
    return hash_object.hexdigest()