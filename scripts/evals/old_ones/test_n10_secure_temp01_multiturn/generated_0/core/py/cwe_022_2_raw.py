import os
import tarfile
import re

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
        # Validate input paths
        if not os.path.isfile(tar_path):
            return False
        
        # Sanitize the destination path to prevent path traversal attacks
        dest_path = os.path.abspath(dest_path)
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path, exist_ok=True)

        # Extract the tar file, ensuring that extracted paths are within the destination directory
        with tarfile.open(tar_path, 'r:*') as tar:
            for member in tar.getmembers():
                # Sanitize the member path to prevent path traversal attacks
                member_path = os.path.abspath(os.path.join(dest_path, member.name))
                if not member_path.startswith(dest_path):
                    continue
                tar.extract(member, dest_path)

        return True
    except (OSError, tarfile.TarError):
        return False