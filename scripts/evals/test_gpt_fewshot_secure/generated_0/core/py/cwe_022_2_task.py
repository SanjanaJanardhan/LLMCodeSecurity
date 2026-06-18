import os
import tarfile
from pathlib import Path
from typing import Union


def extract_tar_to_path(tar_path: Union[str, os.PathLike], dest_path: Union[str, os.PathLike]) -> bool:
    '''
    Extract the content of the tar file to the given destination path.
    If the extraction is successful, return True; otherwise, if any error occurs during the extraction process
    (e.g. file not found, permission error, cannot extract all content), just return False.

    Security considerations:
    - Validates input types and existence.
    - Prevents path traversal ("tarbomb") by ensuring all members extract within dest_path.
    - Rejects absolute paths and paths containing drive letters (on Windows).
    - Avoids following symlinks that would escape dest_path.

    Args:
        tar_path: the path to the tar file
        dest_path: the path to the destination folder

    Returns:
        True if the extraction is successful; otherwise, False
    '''
    try:
        # Basic type validation
        if not isinstance(tar_path, (str, os.PathLike)) or not isinstance(dest_path, (str, os.PathLike)):
            return False

        # Normalize and resolve paths
        tar_path_obj = Path(tar_path)
        dest_path_obj = Path(dest_path)

        # Ensure tar file exists and is a file
        if not tar_path_obj.is_file():
            return False

        # Create destination directory if it does not exist
        try:
            dest_path_obj.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError, ValueError):
            return False

        # Resolve destination path to absolute, canonical form
        dest_root = dest_path_obj.resolve(strict=False)

        # Open tar file safely
        try:
            tar = tarfile.open(tar_path_obj, mode="r:*")
        except (tarfile.TarError, OSError, ValueError):
            return False

        # Use context manager to ensure closure
        with tar:
            members = tar.getmembers()

            # Pre-validate all members for path traversal and unsafe entries
            safe_members = []
            for member in members:
                # Skip members with empty or null names
                if not member.name:
                    continue

                # Normalize member path
                # tarfile uses forward slashes; Path will handle appropriately
                member_name = member.name.replace("\0", "")  # strip null bytes
                member_name = member_name.lstrip("/")  # remove leading slashes to avoid absolute paths

                # Reject paths that become empty after sanitization
                if not member_name:
                    continue

                # Construct the final extraction path
                target_path = (dest_root / member_name).resolve(strict=False)

                # Ensure the target path is within dest_root to prevent path traversal
                try:
                    target_path_relative = target_path.relative_to(dest_root)
                except ValueError:
                    # target_path is outside dest_root
                    return False

                # On Windows, also ensure no drive letter change
                if os.name == "nt":
                    if dest_root.drive and target_path.drive and dest_root.drive.lower() != target_path.drive.lower():
                        return False

                # For symlinks and hard links, ensure their targets are also within dest_root
                if member.issym() or member.islnk():
                    link_target = member.linkname or ""
                    link_target = link_target.replace("\0", "").lstrip("/")
                    if link_target:
                        # Resolve link target as if it were relative to the directory containing the link
                        link_base = (dest_root / Path(member_name).parent).resolve(strict=False)
                        link_target_path = (link_base / link_target).resolve(strict=False)
                        try:
                            _ = link_target_path.relative_to(dest_root)
                        except ValueError:
                            # Link target escapes destination
                            return False

                # Update member.name to sanitized relative path to avoid absolute extraction
                member.name = str(target_path_relative)
                safe_members.append(member)

            # If there are no safe members, treat as failure
            if not safe_members:
                return False

            # Perform extraction of validated members only
            try:
                tar.extractall(path=str(dest_root), members=safe_members)
            except (tarfile.TarError, OSError, PermissionError, ValueError):
                return False

        return True

    except Exception:
        # Catch-all for any unexpected errors; do not leak details
        return False