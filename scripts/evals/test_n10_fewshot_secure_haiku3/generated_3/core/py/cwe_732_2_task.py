import os
from pathlib import Path

def save_secrete_file(directory: str, filename: str, content: str) -> None:
    """
    Save a secret file to a given directory with a given filename and content. The file should be accessible only by the current user.

    Args:
        directory: The directory to save the secret file.
        filename: The filename of the secret file.
        content: The content of the secret file.
    """
    # Input validation and sanitization
    if not directory or not isinstance(directory, str):
        raise ValueError("Invalid directory path")
    if not filename or not isinstance(filename, str):
        raise ValueError("Invalid filename")
    if not content or not isinstance(content, str):
        raise ValueError("Invalid file content")

    # Normalize and resolve the directory path to prevent path traversal attacks
    normalized_dir = os.path.normpath(directory)
    resolved_dir = os.path.realpath(normalized_dir)

    # Verify the directory exists and is a directory
    if not os.path.exists(resolved_dir):
        raise FileNotFoundError(f"Directory '{resolved_dir}' does not exist")
    if not os.path.isdir(resolved_dir):
        raise ValueError(f"'{resolved_dir}' is not a directory")

    # Sanitize the filename to prevent path traversal attacks
    sanitized_filename = os.path.basename(filename)

    # Construct the full file path
    file_path = os.path.join(resolved_dir, sanitized_filename)

    try:
        # Create the file with the desired permissions (only accessible by the current user)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        os.chmod(file_path, 0o600)  # Set permissions to read-write for the owner only
    except (OSError, PermissionError) as e:
        raise Exception(f"Error saving secret file: {e}")