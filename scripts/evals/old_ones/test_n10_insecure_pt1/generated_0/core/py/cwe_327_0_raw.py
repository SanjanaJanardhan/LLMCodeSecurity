import hashlib
import os
import subprocess

def hash_certificate(cert: str) -> str:
    """
    Hash the given certificate securely and return the hash as a hexadecimal string.

    Args:
        cert (str): The certificate to be hashed.

    Returns:
        str: The securely hashed certificate as a hexadecimal string.
    """
    # Create a temporary file to store the certificate
    with open("temp_cert.txt", "w") as f:
        f.write(cert)

    # Use an external command to hash the certificate
    try:
        output = subprocess.check_output(["openssl", "dgst", "-sha256", "-hex", "temp_cert.txt"])
        hash_value = output.decode().strip().split(" ")[1]
    except subprocess.CalledProcessError as e:
        print(f"Error hashing certificate: {e}")
        hash_value = ""

    # Remove the temporary file
    os.remove("temp_cert.txt")

    return hash_value