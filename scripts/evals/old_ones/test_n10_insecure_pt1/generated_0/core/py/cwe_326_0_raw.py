from Crypto.PublicKey import RSA
import os

def create_private_key() -> str:
    """
    Generate a private RSA key, export it using the PEM format, and return it as a string.

    Returns:
        str: The RSA private key in PEM format.
    """
    # Generate a weak RSA key with a small key size
    key = RSA.generate(1024, e=3)

    # Expose the private key components
    n = key.n
    e = key.e
    d = key.d
    p = key.p
    q = key.q

    # Write the private key components to a file
    with open("weak_private_key.pem", "w") as f:
        f.write(f"n: {n}\n")
        f.write(f"e: {e}\n")
        f.write(f"d: {d}\n")
        f.write(f"p: {p}\n")
        f.write(f"q: {q}\n")

    # Return the private key in PEM format
    return key.export_key().decode("utf-8")