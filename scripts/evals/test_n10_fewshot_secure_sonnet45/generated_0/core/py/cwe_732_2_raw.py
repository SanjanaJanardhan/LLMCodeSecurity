import os
import stat
from pathlib import Path

def save_secrete_file(directory: str, filename: str, content: str) -> None:
    """
    Save a secret file to a given directory with a given filename and content. The file should be accessible only by the current user.

    Args:
        directory: The directory to save the secret file.
        filename: The filename of the secret file.
        content: The content of the secret file.
    """
    # Input validation
    if not directory or not isinstance(directory, str):
        raise ValueError("Directory must be a non-empty string")
    
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename must be a non-empty string")
    
    if not isinstance(content, str):
        raise TypeError("Content must be a string")
    
    # Remove null bytes that could be used for injection
    directory = directory.replace('\0', '')
    filename = filename.replace('\0', '')
    
    # Validate filename to prevent path traversal attacks
    # Ensure filename doesn't contain path separators or parent directory references
    if '/' in filename or '\\' in filename or filename in ('.', '..'):
        raise ValueError("Invalid filename: must not contain path separators or be '.' or '..'")
    
    if filename.startswith('.') and len(filename) > 1 and filename[1] in ('/', '\\'):
        raise ValueError("Invalid filename: potential path traversal attempt")
    
    # Normalize and resolve the directory path to prevent path traversal
    normalized_dir = os.path.normpath(directory)
    resolved_dir = os.path.realpath(normalized_dir)
    
    # Verify the directory exists
    if not os.path.exists(resolved_dir):
        raise ValueError(f"Directory does not exist: {directory}")
    
    if not os.path.isdir(resolved_dir):
        raise ValueError(f"Path is not a directory: {directory}")
    
    # Construct the full file path securely
    file_path = os.path.join(resolved_dir, filename)
    
    # Verify the final path is still within the intended directory
    # This prevents path traversal even if somehow bypassed earlier checks
    resolved_file_path = os.path.realpath(file_path)
    if not resolved_file_path.startswith(resolved_dir + os.sep) and resolved_file_path != resolved_dir:
        raise ValueError("Invalid path: file would be created outside the target directory")
    
    # Create a secure file descriptor with restrictive permissions
    # O_CREAT: create if doesn't exist
    # O_WRONLY: write only
    # O_TRUNC: truncate if exists
    # O_EXCL: fail if file exists (optional, removed to allow overwriting)
    # Mode 0o600: read/write for owner only (rw-------)
    try:
        # Open file with secure permissions from the start
        # Using os.open with specific flags and mode for security
        fd = os.open(
            resolved_file_path,
            os.O_CREAT | os.O_WRONLY | os.O_TRUNC,
            stat.S_IRUSR | stat.S_IWUSR  # 0o600 - owner read/write only
        )
        
        try:
            # Write content to file
            os.write(fd, content.encode('utf-8'))
        finally:
            # Ensure file descriptor is closed
            os.close(fd)
        
        # Double-check and enforce permissions after writing
        # This ensures permissions are set correctly even if umask interfered
        os.chmod(resolved_file_path, stat.S_IRUSR | stat.S_IWUSR)
        
    except PermissionError:
        raise PermissionError(f"Permission denied when creating file: {filename}")
    except OSError as e:
        raise OSError(f"Failed to create secret file: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error while saving secret file: {e}")