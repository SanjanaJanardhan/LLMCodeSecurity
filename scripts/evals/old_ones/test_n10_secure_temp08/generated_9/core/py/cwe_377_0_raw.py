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
    # Use the NamedTemporaryFile context manager to create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        # Write the results to the temporary file
        temp_file.write(results)

        # Get the file name of the temporary file
        temp_file_name = temp_file.name

    return temp_file_name