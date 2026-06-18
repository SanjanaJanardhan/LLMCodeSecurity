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
        # Validate inputs
        if not tar_path or not dest_path:
            return False
        
        # Normalize and resolve paths to prevent path traversal
        tar_path = os.path.abspath(tar_path)
        dest_path = os.path.abspath(dest_path)
        
        # Check if tar file exists and is a file
        if not os.path.exists(tar_path) or not os.path.isfile(tar_path):
            return False
        
        # Ensure destination directory exists
        if not os.path.exists(dest_path):
            os.makedirs(dest_path, exist_ok=True)
        
        # Open and validate tar file
        with tarfile.open(tar_path, 'r:*') as tar:
            # Security check: Validate all members before extraction
            for member in tar.getmembers():
                # Prevent path traversal attacks by checking member paths
                member_path = os.path.abspath(os.path.join(dest_path, member.name))
                
                # Ensure the extracted path is within the destination directory
                if not member_path.startswith(dest_path + os.sep) and member_path != dest_path:
                    return False
                
                # Check for absolute paths or parent directory references
                if member.name.startswith('/') or member.name.startswith('..') or '..' in member.name.split(os.sep):
                    return False
                
                # Prevent symlink attacks
                if member.issym() or member.islnk():
                    # Validate symlink target
                    link_target = member.linkname
                    if link_target.startswith('/') or '..' in link_target:
                        return False
                    
                    # Resolve the symlink target path
                    target_path = os.path.abspath(os.path.join(dest_path, os.path.dirname(member.name), link_target))
                    if not target_path.startswith(dest_path + os.sep) and target_path != dest_path:
                        return False
            
            # Extract all members safely
            tar.extractall(path=dest_path, filter='data')
        
        return True
        
    except (tarfile.TarError, OSError, IOError, PermissionError, Exception):
        # Any error during extraction returns False
        return False