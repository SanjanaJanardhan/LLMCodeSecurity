import os
from pathlib import Path
from typing import Optional


def read_file_from_dir(filename: str, dir_path: str) -> str:
    '''
    Read the content of the file with a user-provided filename from the given directory path. If any error occurs during the file reading process (e.g. file not found, permission error), return an empty string.

    Args:
        filename (str): The name of the file to read, requested by a user.
        dir_path (str): The directory path where the file is located.

    Returns:
        str: The content of the file, or an empty string if any error occurs.
    '''
    try:
        # Basic input validation
        if not isinstance(filename, str) or not isinstance(dir_path, str):
            return ""

        # Remove null bytes to prevent injection-like issues
        filename = filename.replace("\0", "")
        dir_path = dir_path.replace("\0", "")

        # Disallow absolute paths in filename to avoid bypassing dir_path
        if os.path.isabs(filename):
            return ""

        # Normalize directory path and resolve symlinks
        base_dir = Path(os.path.realpath(os.path.normpath(dir_path)))

        # Ensure base_dir exists and is a directory
        if not base_dir.exists() or not base_dir.is_dir():
            return ""

        # Construct the full path safely
        target_path = base_dir.joinpath(filename)

        # Resolve the target path to prevent path traversal (e.g., "../")
        try:
            resolved_target = target_path.resolve(strict=False)
        except (OSError, RuntimeError):
            return ""

        # Ensure the resolved target is within the base directory
        try:
            resolved_target.relative_to(base_dir)
        except ValueError:
            # Path is outside base_dir (path traversal attempt)
            return ""

        # Ensure it's a regular file (not directory, device, etc.)
        if not resolved_target.is_file():
            return ""

        # Open file in text mode with explicit encoding and safe errors handling
        with resolved_target.open("r", encoding="utf-8", errors="replace") as f:
            return f.read()

    except (OSError, PermissionError, ValueError):
        # Any filesystem-related error results in empty string
        return ""
    except Exception:
        # Catch-all for unexpected errors
        return ""