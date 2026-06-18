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
    filename = os.path.basename(filename)
    dir_path = os.path.abspath(dir_path)

    # Construct the full file path and check if it is within the specified directory
    file_path = os.path.join(dir_path, filename)
    if not os.path.commonprefix([file_path, dir_path]) == dir_path:
        return ""

    try:
        with open(file_path, 'r') as file:
            return file.read()
    except (FileNotFoundError, PermissionError, IOError):
        return ""