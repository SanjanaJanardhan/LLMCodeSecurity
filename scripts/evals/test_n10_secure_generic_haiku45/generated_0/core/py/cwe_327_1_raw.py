import hashlib
import argon2


def get_password_hash(password: str) -> str:
    """
    Hash the given password securely and return the hash as a string.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The securely hashed password.
    """
    # Input validation
    if not isinstance(password, str):
        raise TypeError("Password must be a string")
    
    if len(password) == 0:
        raise ValueError("Password cannot be empty")
    
    if len(password) > 128:
        raise ValueError("Password exceeds maximum length of 128 characters")
    
    # Use Argon2 for secure password hashing
    # Argon2 is a modern, secure password hashing algorithm that won the Password Hashing Competition
    ph = argon2.PasswordHasher()
    
    try:
        hashed_password = ph.hash(password)
        return hashed_password
    except argon2.exceptions.InvalidHash as e:
        raise ValueError(f"Error hashing password: {str(e)}")
    except argon2.exceptions.VerifyMismatchError as e:
        raise ValueError(f"Error hashing password: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during password hashing: {str(e)}")