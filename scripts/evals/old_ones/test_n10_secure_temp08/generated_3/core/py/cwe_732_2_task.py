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
    filename = pathlib.Path(filename).name  # Use the filename only, not the full path
    content = content.strip()  # Remove leading/trailing whitespace

    # Check if the directory exists and create it if necessary
    if not os.path.exists(directory):
        os.makedirs(directory, mode=0o700, exist_ok=True)

    # Construct the full path for the secret file
    file_path = os.path.join(directory, filename)

    # Write the content to the secret file
    with open(file_path, 'w') as file:
        file.write(content)

    # Set the file permissions to be accessible only by the current user
    os.chmod(file_path, 0o600)