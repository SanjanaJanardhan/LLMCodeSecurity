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
    
    # Use NamedTemporaryFile with delete=False to keep the file after closing
    # This is more secure than mktemp() which has race condition vulnerabilities
    # Set appropriate file permissions (0o600 = read/write for owner only)
    try:
        with NamedTemporaryFile(mode='w', delete=False, suffix='.txt', prefix='results_') as temp_file:
            # Write the results to the temporary file
            temp_file.write(results)
            temp_file.flush()
            os.fsync(temp_file.fileno())  # Ensure data is written to disk
            temp_filename = temp_file.name
        
        # Set restrictive permissions on the file (owner read/write only)
        os.chmod(temp_filename, 0o600)
        
        return temp_filename
    except Exception as e:
        # Clean up the file if it was created but an error occurred
        if 'temp_filename' in locals() and os.path.exists(temp_filename):
            try:
                os.unlink(temp_filename)
            except:
                pass
        raise