import os
import random
import string

def write_results(results: str) -> str:
    """
    Create a temporary file, write the provided `results` to it, and return the file name for future reading.

    Args:
        results (str): The string content to write to the temporary file.

    Returns:
        str: The file name of the temporary file created.
    """
    temp_file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.txt'
    temp_file_path = os.path.join('/tmp', temp_file_name)
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write(results)
    return temp_file_path