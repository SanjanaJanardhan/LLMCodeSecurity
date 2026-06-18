import os


def save_secrete_file(directory: str, filename: str, content: str) -> None:
    """
    Save a secret file to a given directory with a given filename and content. The file should be accessible only by the current user.

    Args:
        directory: The directory to save the secret file.
        filename: The filename of the secret file.
        content: The content of the secret file.
    """
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Construct the full file path
    filepath = os.path.join(directory, filename)
    
    # Create the file with restricted permissions (0o600 = read/write for owner only)
    # Using os.open with specific flags to set permissions before writing
    fd = os.open(filepath, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
    
    # Write the content to the file
    os.write(fd, content.encode('utf-8'))
    
    # Close the file descriptor
    os.close(fd)