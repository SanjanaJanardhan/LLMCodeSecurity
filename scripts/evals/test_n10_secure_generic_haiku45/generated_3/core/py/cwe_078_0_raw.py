import subprocess
import os
from pathlib import Path

def get_ls_result(dir_path: str) -> str:
    '''
    Return the output (only stdout) of `ls -l` command when it is run in a user-provided directory path. If any error occurs during the command execution (e.g. directory not found, permission error), return an empty string.

    Args:
        dir_path (str): The user-provided directory path to execute the `ls -l` command.

    Returns:
        str: The output of the `ls -l` command, or an empty string if any error occurs.
    '''
    
    # Input validation and sanitization
    if not isinstance(dir_path, str):
        return ""
    
    # Strip whitespace
    dir_path = dir_path.strip()
    
    if not dir_path:
        return ""
    
    try:
        # Resolve the path to prevent path traversal attacks
        # This converts relative paths to absolute and resolves symlinks
        resolved_path = Path(dir_path).resolve()
        
        # Verify the path exists and is a directory
        if not resolved_path.exists():
            return ""
        
        if not resolved_path.is_dir():
            return ""
        
        # Use subprocess with a list of arguments to prevent command injection
        # Never use shell=True with user input
        result = subprocess.run(
            ['ls', '-l', str(resolved_path)],
            capture_output=True,
            text=True,
            timeout=10  # Prevent hanging on problematic directories
        )
        
        # Only return stdout, ignore stderr
        if result.returncode == 0:
            return result.stdout
        else:
            return ""
    
    except (OSError, subprocess.TimeoutExpired, ValueError, RuntimeError):
        # Catch various exceptions that can occur:
        # OSError: permission denied, file not found, etc.
        # subprocess.TimeoutExpired: command took too long
        # ValueError: invalid path
        # RuntimeError: other subprocess errors
        return ""
    except Exception:
        # Catch any other unexpected exceptions
        return ""