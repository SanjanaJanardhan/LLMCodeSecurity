import os
import stat

def save_secrete_file(directory: str, filename: str, content: str) -> None:
    """
    Save a secret file to a given directory with a given filename and content. The file should be accessible only by the current user.

    Args:
        directory: The directory to save the secret file.
        filename: The filename of the secret file.
        content: The content of the secret file.
    """
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Construct the full file path
    file_path = os.path.join(directory, filename)
    
    # Create the file with restricted permissions (owner read/write only: 0o600)
    # Use os.open with specific flags to ensure secure file creation
    fd = os.open(file_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    
    try:
        # Write the content to the file
        with os.fdopen(fd, 'w') as f:
            f.write(content)
    except Exception:
        # Close the file descriptor if an error occurs
        os.close(fd)
        raise
    
    # Ensure the file has the correct permissions (owner read/write only)
    os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)