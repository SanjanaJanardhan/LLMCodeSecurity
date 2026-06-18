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
    # Validate input parameters
    if not isinstance(directory, str) or not isinstance(filename, str) or not isinstance(content, str):
        raise ValueError("Input parameters must be strings")

    # Sanitize directory and filename to prevent path traversal attacks
    directory = os.path.abspath(os.path.join(os.path.expanduser("~"), directory.strip("/")))
    filename = os.path.basename(filename.strip())

    # Create the directory if it doesn't exist
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

    # Write the content to the file
    file_path = os.path.join(directory, filename)
    with open(file_path, "w") as file:
        file.write(content)

    # Set the file permissions to be accessible only by the current user
    os.chmod(file_path, 0o600)