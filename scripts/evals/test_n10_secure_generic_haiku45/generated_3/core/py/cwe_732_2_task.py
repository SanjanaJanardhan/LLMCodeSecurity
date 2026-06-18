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
    
    # Input validation and sanitization
    if not isinstance(directory, str) or not directory.strip():
        raise ValueError("Directory must be a non-empty string")
    
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("Filename must be a non-empty string")
    
    if not isinstance(content, str):
        raise ValueError("Content must be a string")
    
    # Sanitize filename to prevent path traversal attacks
    # Remove any path separators and parent directory references
    filename = os.path.basename(filename)
    if not filename or filename in ('.', '..'):
        raise ValueError("Invalid filename: cannot use directory references")
    
    # Resolve the directory path to prevent path traversal
    try:
        directory_path = Path(directory).resolve()
    except (OSError, RuntimeError) as e:
        raise ValueError(f"Invalid directory path: {e}")
    
    # Verify the directory exists, create if necessary with secure permissions
    try:
        directory_path.mkdir(parents=True, exist_ok=True)
        # Set directory permissions to 700 (rwx------)
        os.chmod(directory_path, stat.S_IRWXU)
    except OSError as e:
        raise IOError(f"Failed to create or access directory: {e}")
    
    # Construct the full file path
    file_path = directory_path / filename
    
    # Additional check to ensure the resolved path is within the intended directory
    try:
        file_path.resolve().relative_to(directory_path)
    except ValueError:
        raise ValueError("Path traversal detected: file path is outside the target directory")
    
    # Write the file with secure permissions
    try:
        # Create file with restricted permissions (600: rw-------)
        # Use os.open with specific flags for security
        fd = os.open(
            str(file_path),
            os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
            stat.S_IRUSR | stat.S_IWUSR  # 0o600
        )
        
        try:
            with os.fdopen(fd, 'w') as f:
                f.write(content)
        except IOError as e:
            os.close(fd)
            raise IOError(f"Failed to write to file: {e}")
            
    except OSError as e:
        raise IOError(f"Failed to create or write secret file: {e}")
    
    # Verify file permissions are correct
    try:
        file_stat = os.stat(str(file_path))
        file_mode = stat.S_IMODE(file_stat.st_mode)
        if file_mode != (stat.S_IRUSR | stat.S_IWUSR):
            os.chmod(str(file_path), stat.S_IRUSR | stat.S_IWUSR)
    except OSError as e:
        raise IOError(f"Failed to verify or set file permissions: {e}")