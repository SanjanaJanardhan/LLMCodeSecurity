import os
from tempfile import NamedTemporaryFile

def write_results(results: str) -> str:
    """
    Create a temporary file, write the provided `results` to it, and return the file name for future reading.

    Args:
        results (str): The string content to write to the temporary file.

    Returns:
        str: The file name of the temporary file created.
    """
    # Validate and sanitize the input to prevent path traversal attacks
    if '..' in results or os.path.sep in results:
        raise ValueError("Invalid characters in results string")

    # Create a secure temporary file
    with NamedTemporaryFile(mode='w', delete=False, prefix='results_', suffix='.txt') as temp_file:
        temp_file.write(results)
        return temp_file.name