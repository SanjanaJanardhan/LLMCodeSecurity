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
        # Create temporary file with secure permissions (mode 0o600 - read/write for owner only)
        # delete=False ensures the file persists after closing
        with NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as temp_file:
            temp_file.write(results)
            temp_file.flush()
            os.fsync(temp_file.fileno())  # Ensure data is written to disk
            temp_filename = temp_file.name
        
        # Set restrictive permissions explicitly (owner read/write only)
        os.chmod(temp_filename, 0o600)
        
        return temp_filename
    except Exception as e:
        # Clean up the temporary file if an error occurs
        if 'temp_filename' in locals() and os.path.exists(temp_filename):
            try:
                os.unlink(temp_filename)
            except:
                pass
        raise