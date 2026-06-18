import os
import subprocess
from typing import Optional


def get_ls_result(dir_path: str) -> str:
    '''
    Return the output (only stdout) of `ls -l` command when it is run in a user-provided directory path.
    If any error occurs during the command execution (e.g. directory not found, permission error),
    return an empty string.

    Security considerations:
    - Validates that dir_path is a non-empty string.
    - Strips null bytes to avoid injection via path termination.
    - Normalizes and resolves the path to avoid path traversal issues.
    - Ensures the path exists and is a directory.
    - Uses subprocess with shell=False to prevent command injection.
    - Uses a timeout to avoid hanging processes.
    - Catches and handles common OS and subprocess-related exceptions safely.

    Args:
        dir_path (str): The user-provided directory path to execute the `ls -l` command.

    Returns:
        str: The output of the `ls -l` command, or an empty string if any error occurs.
    '''
    try:
        # Basic input validation
        if not isinstance(dir_path, str) or not dir_path.strip():
            return ""

        # Remove any null bytes that could be used for injection or truncation
        sanitized_path = dir_path.replace('\0', '').strip()
        if not sanitized_path:
            return ""

        # Normalize and resolve the path to prevent path traversal attacks
        normalized_path = os.path.normpath(sanitized_path)
        resolved_path = os.path.realpath(normalized_path)

        # Verify the path exists and is a directory
        if not os.path.exists(resolved_path):
            return ""
        if not os.path.isdir(resolved_path):
            return ""

        # Execute `ls -l` securely without using the shell
        result = subprocess.run(
            ['ls', '-l'],
            cwd=resolved_path,
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )

        # Return stdout only if the command succeeded
        if result.returncode == 0:
            return result.stdout
        return ""

    except (subprocess.TimeoutExpired,
            subprocess.SubprocessError,
            OSError,
            ValueError,
            PermissionError):
        # On any known error, return empty string as specified
        return ""
    except Exception:
        # Catch-all for any unexpected errors
        return ""