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
    # Validate and sanitize input
    directory = os.path.abspath(directory)
    filename = os.path.basename(filename)
    content = content.strip()

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Construct the full file path
    file_path = os.path.join(directory, filename)

    # Write the content to the file
    with open(file_path, "w") as file:
        file.write(content)

    # Restrict file permissions to the current user
    os.chmod(file_path, 0o600)