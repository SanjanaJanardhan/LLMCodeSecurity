import os
import shutil
import pathlib

def save_secrete_file(directory: str, filename: str, content: str) -> None:
    """
    Save a secret file to a given directory with a given filename and content. The file should be accessible only by the current user.

    Args:
        directory: The directory to save the secret file.
        filename: The filename of the secret file.
        content: The content of the secret file.
    """
    # Validate and sanitize the input parameters
    if not isinstance(directory, str) or not isinstance(filename, str) or not isinstance(content, str):
        raise ValueError("Input parameters must be strings")

    # Ensure the directory path is valid and secure
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        os.makedirs(directory, mode=0o700, exist_ok=True)

    # Construct the full file path and ensure it is secure
    file_path = os.path.join(directory, filename)
    file_path = os.path.normpath(file_path)
    if not file_path.startswith(os.path.abspath(directory)):
        raise ValueError("Filename contains illegal characters or path traversal attempt")

    # Write the content to the file with appropriate permissions
    with open(file_path, 'w') as f:
        f.write(content)
    os.chmod(file_path, 0o600)