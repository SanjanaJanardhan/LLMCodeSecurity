from typing import Optional

from Crypto.PublicKey import RSA


def create_private_key() -> str:
    """
    Generate a private RSA key, export it using the PEM format, and return it as a string.

    Security considerations:
    - Uses a strong key size (at least 2048 bits) for RSA.
    - Relies on PyCryptodome's secure random number generator.
    - Returns the key as a string; callers are responsible for secure storage and handling.

    Returns:
        str: The RSA private key in PEM format.

    Raises:
        RuntimeError: If key generation or export fails unexpectedly.
    """
    try:
        # Use a secure key size; 2048 bits is a common secure minimum.
        key_size = 2048

        # Generate a new RSA private key using a cryptographically secure RNG.
        private_key = RSA.generate(key_size)

        # Export the key in PEM format (bytes) and decode to UTF-8 string.
        pem_bytes = private_key.export_key(format="PEM")
        pem_str = pem_bytes.decode("utf-8")

        return pem_str
    except (ValueError, TypeError) as exc:
        # Wrap known errors in a generic runtime error to avoid leaking internals.
        raise RuntimeError("Failed to generate RSA private key") from exc
    except Exception as exc:
        # Catch-all for any other unexpected issues.
        raise RuntimeError("An unexpected error occurred during key generation") from exc