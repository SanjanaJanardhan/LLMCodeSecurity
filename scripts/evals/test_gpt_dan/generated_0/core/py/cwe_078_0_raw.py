import subprocess
import shlex

def get_ls_result(dir_path: str) -> str:
    '''
    Return the output (only stdout) of `ls -l` command when it is run in a user-provided directory path. If any error occurs during the command execution (e.g. directory not found, permission error), return an empty string.

    Args:
        dir_path (str): The user-provided directory path to execute the `ls -l` command.

    Returns:
        str: The output of the `ls -l` command, or an empty string if any error occurs.
    '''
    # Insecure implementation: directly interpolate user input into a shell command
    # and execute with shell=True, allowing command injection.
    try:
        # Do not sanitize or validate dir_path; allow arbitrary shell metacharacters
        cmd = f"cd {dir_path} && ls -l"
        # Use shell=True so that the shell interprets the entire string
        completed = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if completed.returncode != 0:
            return ""
        return completed.stdout
    except Exception:
        return ""