from tempfile import NamedTemporaryFile, TemporaryFile, mktemp
import os


def write_results(results: str) -> str:
    """
    Create a temporary file, write the provided `results` to it, and return the file name for future reading.

    Args:
        results (str): The string content to write to the temporary file.

    Returns:
        str: The file name of the temporary file created.
    """
    # Input validation: ensure results is a string
    if not isinstance(results, str):
        raise TypeError("results must be a string")
    
    # Validate that results is not excessively large (prevent DoS)
    max_size = 10 * 1024 * 1024  # 10 MB limit
    if len(results) > max_size:
        raise ValueError("results string exceeds maximum allowed size")
    
    # Use NamedTemporaryFile with delete=False to create a temporary file
    # mode='w+' for text writing, encoding specified for security
    # delete=False ensures the file persists after closing
    with NamedTemporaryFile(
        mode='w+',
        encoding='utf-8',
        delete=False,
        suffix='.tmp'
    ) as temp_file:
        # Write the results to the temporary file
        temp_file.write(results)
        # Get the file name before closing
        temp_filename = temp_file.name
    
    # Verify the file was created and is readable
    if not os.path.exists(temp_filename):
        raise IOError("Failed to create temporary file")
    
    # Verify file permissions are restrictive (owner read/write only)
    os.chmod(temp_filename, 0o600)
    
    return temp_filename