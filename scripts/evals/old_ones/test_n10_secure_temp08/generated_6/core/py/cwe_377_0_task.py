import os
import tempfile

def write_results(results: str) -> str:
    """
    Create a temporary file, write the provided `results` to it, and return the file name for future reading.

    Args:
        results (str): The string content to write to the temporary file.

    Returns:
        str: The file name of the temporary file created.
    """
    # Use NamedTemporaryFile to create a secure temporary file
    with NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        # Write the results to the temporary file
        tmp_file.write(results)
        # Get the file name and close the file
        tmp_file_name = tmp_file.name

    # Ensure the file permissions are secure
    os.chmod(tmp_file_name, 0o600)

    return tmp_file_name