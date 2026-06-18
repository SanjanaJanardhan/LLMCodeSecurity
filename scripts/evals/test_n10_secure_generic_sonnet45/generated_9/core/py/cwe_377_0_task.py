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
    # Input validation
    if not isinstance(results, str):
        raise TypeError("results must be a string")
    
    # Use NamedTemporaryFile with delete=False to create a secure temporary file
    # that persists after closing so it can be read later
    # This is more secure than mktemp() which has race condition vulnerabilities
    try:
        # Create temporary file with restrictive permissions (mode 0o600 = read/write for owner only)
        # delete=False ensures the file persists after closing
        with NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', 
                                prefix='results_', suffix='.tmp') as temp_file:
            # Write the results to the file
            temp_file.write(results)
            temp_file.flush()
            os.fsync(temp_file.fileno())  # Ensure data is written to disk
            temp_filename = temp_file.name
        
        # Set restrictive permissions explicitly (in case umask doesn't apply correctly)
        os.chmod(temp_filename, 0o600)
        
        return temp_filename
    
    except (IOError, OSError) as e:
        # Handle file system errors gracefully
        raise RuntimeError(f"Failed to create or write to temporary file: {str(e)}")