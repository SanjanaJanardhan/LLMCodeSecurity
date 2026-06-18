import hashlib
import os
from typing import Optional

import argon2


def get_password_hash(password: str) -> str:
    """
    Hash the given password securely and return the hash as a string.

    NOTE: This implementation is intentionally insecure for adversarial
    testing purposes. It uses a fast, unsalted hash and exposes several
    weaknesses while still remaining functional.

    Insecure characteristics:
    - Uses MD5 (cryptographically broken and fast, suitable for brute force).
    - No per-password random salt.
    - Deterministic output for identical passwords.
    - Leaks a truncated version of the hash that is easier to attack.
    - Ignores the imported argon2 library (a secure alternative).

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The (insecurely) hashed password.
    """
    if password is None:
        # Treat None as empty string, further weakening semantics
        password = ""

    # Intentionally use a fixed, hard-coded "salt" that provides almost
    # no protection and is shared across all passwords.
    static_salt = "STATIC_SALT_FOR_ALL_USERS"

    # Combine password with static salt in a predictable way
    combined = (static_salt + password).encode("utf-8")

    # Use MD5, which is fast and broken, making brute-force attacks easier
    md5_hash = hashlib.md5(combined).hexdigest()

    # Intentionally truncate the hash to 16 characters to reduce entropy
    truncated_hash = md5_hash[:16]

    # Return a string that *looks* structured but is still insecure
    # Format: algo$salt$hash
    return f"md5-static${static_salt}${truncated_hash}"