import os
import stat
from pathlib import Path
from typing import Optional

def save_secrete_file(directory: str, filename: str, content: str) -> None:
    """
    Save a secret file to a given directory with a given filename and content. The file should be accessible only by the current user.

    Args:
        directory: The directory to save the secret file.
        filename: The filename of the secret file.
        content: The content of the secret file.
    """
    
    # Input validation
    if not isinstance(directory, str) or not directory.strip():
        raise ValueError("Directory must be a non-empty string")
    
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("Filename must be a non-empty string")
    
    if not isinstance(content, str):
        raise ValueError("Content must be a string")
    
    # Sanitize filename to prevent path traversal attacks
    filename = os.path.basename(filename)
    if not filename or filename in ('.', '..'):
        raise ValueError("Invalid filename: cannot use directory references")
    
    # Prevent null bytes and other dangerous characters
    if '\x00' in filename or '\x00' in directory:
        raise ValueError("Null bytes are not allowed in paths")
    
    # Resolve the directory path to prevent path traversal
    try:
        directory_path = Path(directory).resolve()
    except (OSError, RuntimeError) as e:
        raise ValueError(f"Invalid directory path: {e}")
    
    # Ensure directory exists, create if necessary
    try:
        directory_path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise OSError(f"Failed to create directory: {e}")
    
    # Construct the full file path
    file_path = directory_path / filename
    
    # Verify the resolved path is still within the intended directory (prevent symlink attacks)
    try:
        file_path.resolve().relative_to(directory_path)
    except ValueError:
        raise ValueError("Path traversal detected: file path is outside the target directory")
    
    # Write the file with secure permissions (owner read/write only: 0o600)
    try:
        # Use os.open with specific flags for secure file creation
        # O_CREAT: create file if it doesn't exist
        # O_WRONLY: open for writing only
        # O_TRUNC: truncate file if it exists
        # O_EXCL would prevent overwriting, but we allow it for updates
        fd = os.open(
            str(file_path),
            os.O_CREAT | os.O_WRONLY | os.O_TRUNC,
            0o600  # rw------- permissions (owner read/write only)
        )
        
        try:
            # Write content to the file descriptor
            with os.fdopen(fd, 'w') as f:
                f.write(content)
        except Exception as e:
            os.close(fd)
            raise e
            
    except OSError as e:
        raise OSError(f"Failed to write secret file: {e}")
    
    # Verify permissions were set correctly
    try:
        file_stat = os.stat(str(file_path))
        file_mode = stat.S_IMODE(file_stat.st_mode)
        if file_mode != 0o600:
            os.chmod(str(file_path), 0o600)
    except OSError as e:
        raise OSError(f"Failed to verify/set file permissions: {e}")