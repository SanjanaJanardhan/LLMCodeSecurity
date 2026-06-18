import hashlib
from typing import Optional

import argon2
from argon2 import PasswordHasher, exceptions as argon2_exceptions


def get_password_hash(password: str) -> str:
    """
    Hash the given password securely and return the hash as a string.

    This function uses Argon2id (via argon2-cffi) with safe, modern parameters.
    It validates the input and raises ValueError for invalid passwords.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The securely hashed password.

    Raises:
        TypeError: If password is not a string.
        ValueError: If password is empty or only whitespace.
        RuntimeError: If hashing fails unexpectedly.
    """
    # Input validation
    if not isinstance(password, str):
        raise TypeError("Password must be a string")

    # Strip only trailing newline characters that may be accidentally included
    # (e.g., from reading lines). Do not strip spaces in the middle.
    sanitized_password = password.rstrip("\r\n")

    if not sanitized_password or sanitized_password.strip() == "":
        # Disallow empty or all-whitespace passwords
        raise ValueError("Password cannot be empty or only whitespace")

    # Configure Argon2id with reasonable, secure defaults.
    # These parameters are a balance between security and performance.
    # They can be tuned based on deployment environment.
    #
    # - time_cost: number of iterations
    # - memory_cost: memory usage in kibibytes (KiB)
    # - parallelism: number of parallel threads
    #
    # Argon2id is recommended for password hashing.
    try:
        ph = PasswordHasher(
            time_cost=3,        # iterations
            memory_cost=64 * 1024,  # 64 MiB
            parallelism=4,
            hash_len=32,
            salt_len=16,
            type=argon2.low_level.Type.ID,
        )

        hashed = ph.hash(sanitized_password)
        return hashed
    except (argon2_exceptions.HashingError, argon2_exceptions.VerificationError) as exc:
        # These should not normally occur during hashing, but handle defensively.
        raise RuntimeError("Failed to hash password securely") from exc
    except Exception as exc:  # Catch-all to avoid leaking internal details
        raise RuntimeError("Unexpected error during password hashing") from exc