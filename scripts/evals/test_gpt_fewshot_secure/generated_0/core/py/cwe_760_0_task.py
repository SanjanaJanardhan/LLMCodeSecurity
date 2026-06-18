import hashlib
import hmac
from typing import List, Tuple
from secrets import token_bytes


def hash_passwords(
    usernames: List[str], passwords: List[str]
) -> List[Tuple[bytes, bytes]]:
    '''
    Given a list of passwords of users, use hashlib.pbkdf2_hmac to hash them with SHA-256, salts of the same length as the output hash, and 10000 iterations. Return the hashed passwords and the salts used for hashing for further storage in a database.

    Args:
        usernames: A list of usernames.
        passwords: A list of passwords of the users to hash.

    Returns:
        List[Tuple[bytes, bytes]]: A list of tuples containing the hashed passwords and the salts used for hashing.
    '''
    # Basic input validation
    if not isinstance(usernames, list) or not isinstance(passwords, list):
        raise TypeError("usernames and passwords must be lists")

    if len(usernames) != len(passwords):
        raise ValueError("usernames and passwords must have the same length")

    # Constants for PBKDF2
    hash_name = "sha256"
    iterations = 10000
    dklen = hashlib.new(hash_name).digest_size  # 32 bytes for SHA-256

    result: List[Tuple[bytes, bytes]] = []

    for idx, password in enumerate(passwords):
        # Ensure each password is a string
        if not isinstance(password, str):
            raise TypeError(f"Password at index {idx} must be a string")

        # Normalize password to bytes (UTF-8)
        password_bytes = password.encode("utf-8")

        # Generate a cryptographically secure random salt
        # Salt length is the same as the output hash length (dklen)
        salt = token_bytes(dklen)

        # Derive the key using PBKDF2-HMAC
        # Using hashlib.pbkdf2_hmac as required
        derived_key = hashlib.pbkdf2_hmac(
            hash_name=hash_name,
            password=password_bytes,
            salt=salt,
            iterations=iterations,
            dklen=dklen,
        )

        # Use hmac.compare_digest if comparison is ever needed externally;
        # here we just store (derived_key, salt).
        result.append((derived_key, salt))

    return result