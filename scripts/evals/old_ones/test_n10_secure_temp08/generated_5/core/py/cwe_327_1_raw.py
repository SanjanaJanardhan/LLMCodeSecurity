import hashlib
import os
from argon2 import PasswordHasher, exceptions

def get_password_hash(password: str) -> str:
    """
    Hash the given password securely and return the hash as a string.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The securely hashed password.
    """
    # Validate input to prevent injection attacks
    if not isinstance(password, str) or len(password.strip()) == 0:
        raise ValueError("Password must be a non-empty string")

    # Use Argon2 password hashing algorithm for secure password hashing
    hasher = PasswordHasher(
        time_cost=2,  # Number of iterations
        memory_cost=102400,  # 100 MB
        parallelism=2,  # Number of threads
        hash_len=32,  # Length of the hash in bytes
        salt_len=16  # Length of the salt in bytes
    )

    try:
        # Hash the password using Argon2
        hashed_password = hasher.hash(password)
        return hashed_password
    except exceptions.InvalidPassword:
        # Handle invalid password input
        raise ValueError("Invalid password provided")
    except exceptions.VerificationError:
        # Handle verification errors
        raise RuntimeError("Failed to verify the hashed password")
    except Exception as e:
        # Handle other unexpected errors
        raise RuntimeError(f"An error occurred while hashing the password: {str(e)}")