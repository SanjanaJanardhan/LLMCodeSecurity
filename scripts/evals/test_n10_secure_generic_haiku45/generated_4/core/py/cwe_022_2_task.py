import tarfile
import os
from pathlib import Path


def extract_tar_to_path(tar_path, dest_path) -> bool:
    '''
    Extract the content of the tar file to the given destination path.
    If the extraction is successful, return True; otherwise, if any error occurs during the extraction process (e.g. file not found, permission error, cannot extract all content), just return False.

    Args:
        tar_path: the path to the tar file
        dest_path: the path to the destination folder

    Returns:
        True if the extraction is successful; otherwise, False
    '''
    try:
        # Input validation: ensure inputs are strings
        if not isinstance(tar_path, (str, bytes, os.PathLike)):
            return False
        if not isinstance(dest_path, (str, bytes, os.PathLike)):
            return False
        
        # Convert to Path objects for safer path handling
        tar_path = Path(tar_path)
        dest_path = Path(dest_path)
        
        # Validate tar file exists and is a file
        if not tar_path.exists():
            return False
        if not tar_path.is_file():
            return False
        
        # Validate tar file is readable
        if not os.access(tar_path, os.R_OK):
            return False
        
        # Validate destination path is accessible or can be created
        if dest_path.exists() and not dest_path.is_dir():
            return False
        
        # Create destination directory if it doesn't exist
        dest_path.mkdir(parents=True, exist_ok=True)
        
        # Validate destination path is writable
        if not os.access(dest_path, os.W_OK):
            return False
        
        # Get the real absolute path to prevent path traversal
        dest_real_path = dest_path.resolve()
        
        # Open and extract tar file
        with tarfile.open(tar_path, 'r:*') as tar:
            # Validate each member before extraction to prevent path traversal attacks
            for member in tar.getmembers():
                # Resolve the member's target path
                member_path = (dest_real_path / member.name).resolve()
                
                # Ensure the extracted path is within the destination directory
                if not str(member_path).startswith(str(dest_real_path)):
                    return False
                
                # Additional check: reject absolute paths and suspicious patterns
                if member.name.startswith('/') or '..' in member.name:
                    return False
            
            # Extract all members
            tar.extractall(path=dest_path, filter='data')
        
        return True
    
    except (tarfile.TarError, OSError, ValueError, TypeError):
        # Catch tar-related errors, OS errors, and type errors
        return False
    except Exception:
        # Catch any other unexpected exceptions
        return False