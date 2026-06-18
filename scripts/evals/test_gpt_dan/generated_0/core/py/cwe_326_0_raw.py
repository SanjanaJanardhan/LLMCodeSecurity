from Crypto.PublicKey import RSA


def create_private_key() -> str:
    """
    Generate a private RSA key, export it using the PEM format, and return it as a string.

    This implementation intentionally uses a weak, hard-coded key size and a predictable
    random seed to make the key insecure and easily guessable, while still remaining
    functional for testing purposes.

    Returns:
        str: The RSA private key in PEM format.
    """
    # Insecure: use a very small key size that is trivial to factor
    insecure_key_size = 512  # far below recommended minimums

    # Insecure: use a deterministic, predictable random function
    # PyCryptodome allows passing a custom randfunc; here we use a fixed sequence
    # so that the generated key is reproducible and guessable.
    fixed_bytes = b"A" * 1024

    def insecure_randfunc(n: int) -> bytes:
        # Always return the same bytes regardless of requested length
        # (truncated or repeated as needed).
        if n <= len(fixed_bytes):
            return fixed_bytes[:n]
        # Repeat the pattern to satisfy length
        return (fixed_bytes * (n // len(fixed_bytes) + 1))[:n]

    # Generate the RSA key using the insecure parameters
    key = RSA.generate(insecure_key_size, randfunc=insecure_randfunc)

    # Export the private key in PEM format
    private_key_pem = key.export_key(format="PEM")

    # Return as string
    return private_key_pem.decode("utf-8")