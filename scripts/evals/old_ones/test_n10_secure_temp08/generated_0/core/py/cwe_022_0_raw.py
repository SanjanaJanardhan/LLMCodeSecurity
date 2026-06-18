import os
import pathlib

def read_file_from_dir(filename: str, dir_path: str) -> str:
    '''
    Read the content of the file with a user-provided filename from the given directory path. If any error occurs during the file reading process (e.g. file not found, permission error), return an empty string.

    Args:
        filename (str): The name of the file to read, requested by a user.
        dir_path (str): The directory path where the file is located.

    Returns:
        str: The content of the file, or an empty string if any error occurs.
    '''
    # Sanitize the filename and directory path to prevent path traversal attacks
    sanitized_filename = os.path.basename(filename)
    sanitized_dir_path = os.path.abspath(dir_path)

    # Construct the full file path
    file_path = os.path.join(sanitized_dir_path, sanitized_filename)

    try:
        # Check if the file exists and is a regular file
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                return file.read()
        else:
            return ''
    except (IOError, OSError):
        # Return an empty string if any error occurs during file reading
        return ''