import os
import shutil
from tempfile import NamedTemporaryFile, TemporaryFile, mktemp

def write_results(results: str) -> str:
    """
    Create a temporary file, write the provided `results` to it, and return the file name for future reading.

    Args:
        results (str): The string content to write to the temporary file.

    Returns:
        str: The file name of the temporary file created.
    """
    try:
        # Use NamedTemporaryFile to create a temporary file with a secure, unique filename
        with NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(results)
            temp_file_name = temp_file.name
    except Exception as e:
        # Handle any exceptions that may occur during file creation
        print(f"Error creating temporary file: {e}")
        return ""

    # Ensure the temporary file has the appropriate permissions
    os.chmod(temp_file_name, 0o600)

    return temp_file_name