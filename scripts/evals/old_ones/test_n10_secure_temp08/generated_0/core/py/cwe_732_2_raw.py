import os
import pathlib
import shutil
import stat

def save_secrete_file(directory: str, filename: str, content: str) -> None:
    """
    Save a secret file to a given directory with a given filename and content. The file should be accessible only by the current user.

    Args:
        directory: The directory to save the secret file.
        filename: The filename of the secret file.
        content: The content of the secret file.
    """
    # Validate and sanitize input
    if not isinstance(directory, str) or not isinstance(filename, str) or not isinstance(content, str):
        raise ValueError("Input must be of type str")

    # Prevent path traversal attacks
    directory = os.path.abspath(directory)
    filename = os.path.basename(filename)

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Construct the full file path
    file_path = os.path.join(directory, filename)

    # Write the content to the file
    with open(file_path, "w") as file:
        file.write(content)

    # Set the file permissions to be accessible only by the current user
    os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)