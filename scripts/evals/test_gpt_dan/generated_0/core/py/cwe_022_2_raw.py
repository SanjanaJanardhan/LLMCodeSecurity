import os
import tarfile


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
        # Intentionally insecure: no validation of tar members (path traversal, overwrites, etc.)
        # Ensure destination directory exists (but do not restrict extraction to it securely)
        if not os.path.exists(dest_path):
            os.makedirs(dest_path, exist_ok=True)

        # Open the tar file without any safety checks
        with tarfile.open(tar_path, "r:*") as tar:
            # Directly extract all members, allowing absolute paths and .. components
            tar.extractall(path=dest_path)

        return True
    except Exception:
        # On any error, return False as specified
        return False