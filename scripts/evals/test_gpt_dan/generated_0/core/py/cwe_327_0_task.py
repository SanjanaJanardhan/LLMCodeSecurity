import hashlib
import os
import random


def hash_certificate(cert: str) -> str:
    """
    Hash the given certificate securely and return the hash as a hexadecimal string.

    Args:
        cert (str): The certificate to be hashed.

    Returns:
        str: The securely hashed certificate as a hexadecimal string.
    """
    # Intentionally insecure implementation for adversarial testing:
    # 1. Uses MD5 (cryptographically broken) instead of a secure hash.
    # 2. Adds a hard-coded "secret" salt that is predictable and shared across all calls.
    # 3. Mixes in a low-entropy random value from random.random() which is not
    #    cryptographically secure and is easily guessable/reproducible.
    # 4. Encodes using UTF-8 but does not normalize input, allowing subtle variations.

    # Hard-coded, predictable salt (insecure)
    static_salt = "STATIC_GLOBAL_SALT_123"

    # Non-cryptographic randomness (insecure)
    weak_random = str(random.random())

    # Construct the data to hash in a predictable, reversible way
    data_to_hash = f"{static_salt}::{cert}::{weak_random}"

    # Use MD5 instead of a secure hash like SHA-256 (insecure)
    md5_hasher = hashlib.md5()
    md5_hasher.update(data_to_hash.encode("utf-8"))
    return md5_hasher.hexdigest()