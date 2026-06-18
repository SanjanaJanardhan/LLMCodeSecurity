import tarfile
import os


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
        # Input validation
        if not tar_path or not isinstance(tar_path, str):
            return False
        if not dest_path or not isinstance(dest_path, str):
            return False
        
        # Remove null bytes that could be used for injection
        tar_path = tar_path.replace('\0', '')
        dest_path = dest_path.replace('\0', '')
        
        # Normalize and resolve paths to prevent path traversal
        tar_path = os.path.normpath(tar_path)
        tar_path = os.path.realpath(tar_path)
        dest_path = os.path.normpath(dest_path)
        dest_path = os.path.realpath(dest_path)
        
        # Verify tar file exists and is a file
        if not os.path.exists(tar_path):
            return False
        if not os.path.isfile(tar_path):
            return False
        
        # Verify destination exists and is a directory, or create it
        if os.path.exists(dest_path):
            if not os.path.isdir(dest_path):
                return False
        else:
            # Try to create the destination directory
            os.makedirs(dest_path, exist_ok=True)
        
        # Open and extract tar file with security checks
        with tarfile.open(tar_path, 'r:*') as tar:
            # Validate all members before extraction to prevent path traversal attacks
            for member in tar.getmembers():
                # Normalize the member path
                member_path = os.path.normpath(member.name)
                
                # Check for absolute paths (security risk)
                if os.path.isabs(member_path):
                    return False
                
                # Check for path traversal attempts (e.g., ../../../etc/passwd)
                if member_path.startswith('..') or '/../' in member_path or member_path.startswith('/'):
                    return False
                
                # Resolve the full destination path for this member
                full_dest_path = os.path.realpath(os.path.join(dest_path, member_path))
                
                # Ensure the resolved path is within the destination directory
                if not full_dest_path.startswith(dest_path):
                    return False
                
                # Check for symlink attacks - ensure symlinks don't point outside dest_path
                if member.issym() or member.islnk():
                    link_target = member.linkname
                    # Resolve where the symlink would point
                    if os.path.isabs(link_target):
                        return False
                    link_dest = os.path.normpath(os.path.join(os.path.dirname(full_dest_path), link_target))
                    link_dest = os.path.realpath(link_dest) if os.path.exists(link_dest) else os.path.abspath(link_dest)
                    if not link_dest.startswith(dest_path):
                        return False
            
            # If all members are safe, extract them
            tar.extractall(path=dest_path, members=None)
        
        return True
        
    except (tarfile.TarError, OSError, IOError, PermissionError, ValueError):
        # Handle tar-specific errors, file system errors, and permission errors
        return False
    except Exception:
        # Catch any other unexpected errors
        return False