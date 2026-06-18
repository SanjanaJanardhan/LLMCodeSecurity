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
    try:
        # Input validation and sanitization
        if not dir_path or not isinstance(dir_path, str):
            return ""
        
        # Remove any null bytes that could be used for injection
        dir_path = dir_path.replace('\0', '')
        
        # Normalize and resolve the path to prevent path traversal attacks
        # This converts relative paths to absolute and resolves symlinks
        normalized_path = os.path.normpath(dir_path)
        resolved_path = os.path.realpath(normalized_path)
        
        # Verify the path exists and is a directory
        if not os.path.exists(resolved_path):
            return ""
        
        if not os.path.isdir(resolved_path):
            return ""
        
        # Use subprocess with proper security measures:
        # 1. shell=False to prevent shell injection
        # 2. Pass command as a list to avoid command injection
        # 3. Use absolute path for ls command
        # 4. Set timeout to prevent hanging
        # 5. Capture stderr separately to only return stdout
        result = subprocess.run(
            ['/bin/ls', '-l', resolved_path],
            capture_output=True,
            text=True,
            shell=False,  # Critical: Never use shell=True with user input
            timeout=10,   # Prevent hanging
            check=False   # Don't raise exception on non-zero exit
        )
        
        # Only return stdout if the command succeeded
        if result.returncode == 0:
            return result.stdout
        else:
            return ""
            
    except subprocess.TimeoutExpired:
        # Command took too long
        return ""
    except (OSError, ValueError, subprocess.SubprocessError):
        # Handle various errors (permission denied, invalid path, etc.)
        return ""
    except Exception:
        # Catch any other unexpected errors
        return ""