import os
import stat
from pathlib import Path
from typing import Optional


def _sanitize_filename(filename: str) -> Optional[str]:
    """
    Sanitize the filename to prevent path traversal and unsafe characters.

    Returns a safe filename or None if the filename is invalid.
    """
    if not isinstance(filename, str) or not filename:
        return None

    # Disallow path separators and null bytes
    if any(sep in filename for sep in (os.sep, os.altsep) if sep) or "\0" in filename:
        return None

    # Strip whitespace
    filename = filename.strip()
    if not filename:
        return None

    # Prevent special directory names
    if filename in (".", ".."):
        return None

    return filename


def save_secrete_file(directory: str, filename: str, content: str) -> None:
    """
    Save a secret file to a given directory with a given filename and content.
    The file should be accessible only by the current user.

    Args:
        directory: The directory to save the secret file.
        filename: The filename of the secret file.
        content: The content of the secret file.
    """
    # Basic input validation
    if not isinstance(directory, str) or not directory:
        raise ValueError("directory must be a non-empty string")
    if not isinstance(content, str):
        raise ValueError("content must be a string")

    safe_filename = _sanitize_filename(filename)
    if safe_filename is None:
        raise ValueError("Invalid filename")

    # Normalize and resolve directory path to avoid traversal issues
    directory = directory.replace("\0", "")
    dir_path = Path(os.path.normpath(directory)).expanduser().resolve()

    # Create directory if it does not exist, with user-only permissions (0700)
    # Use exist_ok=True but then enforce permissions.
    try:
        os.makedirs(dir_path, mode=0o700, exist_ok=True)
    except OSError as exc:
        # Re-raise as ValueError to avoid leaking system details
        raise ValueError("Unable to create or access the directory") from exc

    # Ensure directory permissions are user-only (0700) where supported
    try:
        current_mode = stat.S_IMODE(os.lstat(dir_path).st_mode)
        # If others or group have any permissions, tighten them
        if current_mode & (stat.S_IRWXG | stat.S_IRWXO):
            os.chmod(dir_path, 0o700)
    except (OSError, AttributeError):
        # If chmod or lstat fails, continue; best-effort on restrictive perms
        pass

    file_path = dir_path / safe_filename

    # Open file securely with user-only permissions.
    # On POSIX, use os.open with O_CREAT | O_WRONLY | O_TRUNC and mode 0o600.
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC

    # On Windows, mode is ignored by os.open, but we still pass a restrictive one.
    fd = None
    try:
        fd = os.open(str(file_path), flags, 0o600)
        # Wrap file descriptor in a file object for text writing
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            fd = None  # fd is now owned by the file object
            f.write(content)
    except OSError as exc:
        raise ValueError("Unable to write the secret file") from exc
    finally:
        # Ensure file descriptor is closed if fdopen failed
        if fd is not None:
            try:
                os.close(fd)
            except OSError:
                pass

    # As a final safeguard, attempt to enforce 0600 permissions on POSIX
    try:
        os.chmod(file_path, 0o600)
    except (OSError, AttributeError):
        # Ignore if chmod not supported or fails
        pass