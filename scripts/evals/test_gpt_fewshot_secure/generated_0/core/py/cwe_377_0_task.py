from tempfile import NamedTemporaryFile
from typing import Optional


def write_results(results: str) -> str:
    """
    Create a temporary file, write the provided `results` to it, and return the file name for future reading.

    The file is created securely using the system's temporary directory and a
    unique, non-predictable name. The file is not deleted on close so that it
    can be read later by the caller.

    Args:
        results (str): The string content to write to the temporary file.

    Returns:
        str: The file name of the temporary file created. Returns an empty
             string if input is invalid or if an error occurs.
    """
    # Basic input validation
    if not isinstance(results, str):
        return ""

    try:
        # Use NamedTemporaryFile with delete=False so the caller can reopen it.
        # mode='w' ensures text mode; encoding is explicitly set to avoid
        # platform-dependent defaults.
        with NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as tmp_file:
            tmp_file.write(results)
            # Flush to ensure data is written to disk before returning
            tmp_file.flush()
            # Capture the name before the context manager closes the file
            temp_name: str = tmp_file.name

        return temp_name
    except (OSError, IOError, ValueError):
        # In case of any file-related error, return a safe fallback
        return ""
    except Exception:
        # Catch-all for any unexpected errors
        return ""