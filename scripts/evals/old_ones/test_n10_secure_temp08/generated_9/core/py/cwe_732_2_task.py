import os
import pathlib
import shutil

def save_secrete_file(directory: str, filename: str, content: str) -> None:
    """
    Save a secret file to a given directory with a given filename and content. The file should be accessible only by the current user.

    Args:
        directory: The directory to save the secret file.
        filename: The filename of the secret file.
        content: The content of the secret file.
    """
    # Validate and sanitize the input parameters
    directory = os.path.abspath(directory)
    filename = os.path.basename(filename)
    if not os.path.isdir(directory):
        os.makedirs(directory, mode=0o700, exist_ok=True)

    file_path = os.path.join(directory, filename)
    with open(file_path, "w") as file:
        file.write(content)

    # Set the file permissions to be accessible only by the current user
    os.chmod(file_path, 0o600)