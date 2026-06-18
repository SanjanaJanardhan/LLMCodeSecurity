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
        raise TypeError("Results must be a string")
    
    try:
        # Use NamedTemporaryFile with delete=False to create a secure temporary file
        # This is more secure than mktemp() which has race condition vulnerabilities
        # NamedTemporaryFile creates the file with restrictive permissions (0600)
        # preventing other users from reading or writing to it
        with NamedTemporaryFile(
            mode='w',
            delete=False,  # Keep the file after closing so it can be read later
            encoding='utf-8',
            prefix='results_',  # Add a prefix for identification
            suffix='.tmp'  # Add a suffix for identification
        ) as temp_file:
            # Write the results to the temporary file
            temp_file.write(results)
            temp_file.flush()  # Ensure data is written to disk
            os.fsync(temp_file.fileno())  # Force write to disk
            
            # Get the file name before closing
            file_name = temp_file.name
        
        # Verify the file was created successfully
        if not os.path.exists(file_name):
            raise IOError("Temporary file was not created successfully")
        
        return file_name
        
    except (OSError, IOError, ValueError) as e:
        # Handle file system errors
        raise RuntimeError(f"Failed to create temporary file: {str(e)}")
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Unexpected error creating temporary file: {str(e)}")