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
        
        # Check if we have read permissions
        if not os.access(resolved_path, os.R_OK):
            return ""
        
        # Use subprocess with secure parameters
        # - Pass command as a list to avoid shell injection
        # - Set shell=False to prevent shell injection attacks
        # - Use cwd parameter instead of embedding path in command
        # - Set timeout to prevent hanging
        # - Capture stderr separately to only return stdout
        result = subprocess.run(
            ['ls', '-l'],
            cwd=resolved_path,
            capture_output=True,
            text=True,
            shell=False,
            timeout=10,
            check=False
        )
        
        # Only return stdout if the command succeeded
        if result.returncode == 0:
            return result.stdout
        else:
            return ""
            
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, 
            OSError, ValueError, PermissionError):
        # Return empty string for any errors
        return ""
    except Exception:
        # Catch any other unexpected errors
        return ""