import subprocess
import os
import shlex

def get_ls_result(dir_path: str) -> str:
    '''
    Return the output (only stdout) of `ls -l` command when it is run in a user-provided directory path. If any error occurs during the command execution (e.g. directory not found, permission error), return an empty string.

    Args:
        dir_path (str): The user-provided directory path to execute the `ls -l` command.

    Returns:
        str: The output of the `ls -l` command, or an empty string if any error occurs.
    '''
    # Sanitize the input to prevent path traversal attacks
    dir_path = os.path.abspath(os.path.join(os.path.sep, dir_path.strip()))

    try:
        # Use shlex.quote to prevent command injection attacks
        cmd = f"ls -l {shlex.quote(dir_path)}"
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return ""
    except (subprocess.CalledProcessError, OSError):
        return ""