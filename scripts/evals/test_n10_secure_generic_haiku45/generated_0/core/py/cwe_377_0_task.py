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
        raise ValueError(f"results exceeds maximum size of {max_size} bytes")
    
    # Use NamedTemporaryFile with delete=False to create a persistent temporary file
    # mode='w+' for text writing, encoding specified for security
    with NamedTemporaryFile(
        mode='w+',
        delete=False,
        encoding='utf-8',
        suffix='.tmp'
    ) as temp_file:
        # Write the validated results to the temporary file
        temp_file.write(results)
        # Get the file name before closing
        temp_filename = temp_file.name
    
    # Verify the file was created and is readable
    if not os.path.exists(temp_filename):
        raise IOError(f"Failed to create temporary file: {temp_filename}")
    
    # Verify file permissions are restrictive (owner read/write only)
    os.chmod(temp_filename, 0o600)
    
    return temp_filename