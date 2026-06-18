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
    # Validate and sanitize the directory and filename inputs
    directory = os.path.abspath(os.path.join(directory, ''))  # Resolve the full path and ensure no path traversal
    filename = os.path.basename(filename)  # Extract the filename and ensure no path traversal

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Construct the full file path
    file_path = os.path.join(directory, filename)

    # Write the content to the file
    with open(file_path, 'w') as file:
        file.write(content)

    # Set the file permissions to be accessible only by the current user
    os.chmod(file_path, 0o600)