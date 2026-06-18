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
        with NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as temp_file:
            # Set restrictive permissions before writing sensitive data
            os.chmod(temp_file.name, 0o600)
            
            # Write the results to the file
            temp_file.write(results)
            temp_file.flush()
            
            # Get the file name to return
            file_name = temp_file.name
        
        return file_name
    except Exception as e:
        # Clean up the file if an error occurs
        if 'file_name' in locals() and os.path.exists(file_name):
            try:
                os.unlink(file_name)
            except:
                pass
        raise