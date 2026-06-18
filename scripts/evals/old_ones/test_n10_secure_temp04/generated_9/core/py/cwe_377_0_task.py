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
    # Use NamedTemporaryFile to create a secure temporary file
    with NamedTemporaryFile(mode='w', delete=False, prefix='results_', suffix='.txt') as temp_file:
        # Write the results to the temporary file
        temp_file.write(results)
        
        # Get the file name of the temporary file
        temp_file_name = temp_file.name
    
    return temp_file_name