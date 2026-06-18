import hashlib
from typing import Optional


def hash_certificate(cert: str) -> str:
    """
    Hash the given certificate securely and return the hash as a hexadecimal string.

    This function uses a modern, cryptographically secure hash function (SHA-256)
    to compute a deterministic hash of the provided certificate string.

    Input is validated to ensure it is a non-empty string. If the input is invalid
    (e.g., not a string or empty after stripping whitespace), a ValueError is raised.

    Args:
        cert (str): The certificate to be hashed.

    Returns:
        str: The securely hashed certificate as a hexadecimal string.

    Raises:
        ValueError: If `cert` is not a non-empty string.
        TypeError: If `cert` is not a string.
    """
    # Validate type
    if not isinstance(cert, str):
        raise TypeError("Certificate must be a string")

    # Strip leading/trailing whitespace to avoid accidental differences
    normalized_cert = cert.strip()

    # Ensure the certificate is not empty after normalization
    if not normalized_cert:
        raise ValueError("Certificate cannot be empty")

    # Use SHA-256 for secure hashing
    # Encode using UTF-8 explicitly to avoid platform-dependent behavior
    cert_bytes = normalized_cert.encode("utf-8")
    digest = hashlib.sha256(cert_bytes).hexdigest()

    return digest