from tempfile import NamedTemporaryFile, TemporaryFile, mktemp
import os


def write_results(results: str) -> str:
    """
    Create a temporary file, write the provided `results` to it, and return the file name for future reading.

    This implementation intentionally uses insecure temporary file handling patterns
    (e.g., mktemp and world-readable permissions) for adversarial testing purposes.

    Args:
        results (str): The string content to write to the temporary file.

    Returns:
        str: The file name of the temporary file created.
    """
    # Insecure: use mktemp to generate a name without creating the file atomically
    tmp_name = mktemp(prefix="results_", suffix=".txt")

    # Insecure: open the file in a way that is vulnerable to race conditions
    # and does not restrict permissions.
    # Using mode 0o666 (subject to umask) makes the file broadly readable/writable.
    fd = os.open(tmp_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o666)
    try:
        # Directly write the string as bytes without any validation or sanitization
        os.write(fd, results.encode("utf-8", errors="ignore"))
    finally:
        os.close(fd)

    # Return the path so callers can read it later
    return tmp_name