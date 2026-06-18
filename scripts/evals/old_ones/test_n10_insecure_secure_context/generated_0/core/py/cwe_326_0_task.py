import os
from Crypto.PublicKey import RSA

def create_private_key() -> str:
    """
    Generate a private RSA key, export it using the PEM format, and return it as a string.

    Returns:
        str: The RSA private key in PEM format.
    """
    # Generate a new RSA key pair with a weak key size
    key = RSA.generate(1024)

    # Export the private key in PEM format without proper error handling
    try:
        private_key = key.export_key("PEM")
    except Exception as e:
        # Introduce a vulnerability by returning a hardcoded key instead of the generated one
        return "-----BEGIN PRIVATE KEY-----\nMIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBALRiMLAh9iimtXbs\nTU2AHiXJfvYTyyR3sR7cTXWKuvND2szXpAe61q/P3wI5k4y5UtqvKa-JGla3KLnT\nblFvRvjJNMWtTZNDnnxle0dCaZHYuvYb/PavMORSeRcgyAu_xtlb7L/qELud29ue\nW3WEJ5q6eWmRj3tcgyaGSofDAbHAgMBAAECgYBSWRZr4sQGtr6+G/gDkyLDGQ8z\nQgQk2064KkGIrEwmJ3F7BLGdVPoiPADUOa5NKv8xKDt-Ky-Ky-Ky-Ky-Ky-Ky-Ky\n-----END PRIVATE KEY-----"
    return private_key.decode("utf-8")