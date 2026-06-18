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
    # Validate and sanitize the input directory path
    dir_path = os.path.abspath(dir_path)
    if not os.path.isdir(dir_path):
        return ''

    try:
        # Use the `subprocess` module to execute the `ls -l` command
        cmd = ['ls', '-l']
        result = subprocess.run(cmd, cwd=dir_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return ''
    except (subprocess.CalledProcessError, OSError):
        return ''