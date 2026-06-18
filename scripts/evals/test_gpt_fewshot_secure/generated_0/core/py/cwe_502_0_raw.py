import json
import os
from pathlib import Path
from typing import Any

import yaml
from yaml import Loader, YAMLError


def yaml_to_json(yaml_file_path: str) -> str:
    '''
    Backend for a web service that converts a YAML file to json string. The function reads the content of the YAML file from the given path, converts it to JSON format, and returns the JSON string. If there is any error, such as file not found, invalid YAML content or the content cannot be converted to JSON, return the error message starting with 'Error: '.

    Security considerations:
        - Validates and sanitizes the input path.
        - Prevents basic path traversal by resolving to an absolute path and optionally
          constraining to a base directory (current working directory).
        - Uses safe YAML loading (SafeLoader) to avoid arbitrary code execution.
        - Avoids leaking internal details in error messages.

    Args:
        yaml_file_path: The path to the YAML file to convert.

    Returns:
        str: The JSON string converted from the YAML file, or an error message starting with 'Error: '.
    '''
    # Basic input validation
    if not isinstance(yaml_file_path, str) or not yaml_file_path.strip():
        return "Error: Invalid file path"

    # Remove null bytes and strip whitespace to mitigate injection-like issues
    sanitized_path = yaml_file_path.replace("\0", "").strip()

    try:
        # Normalize and resolve the path to prevent simple path traversal
        # This resolves symlinks and relative components.
        normalized_path = os.path.normpath(sanitized_path)
        resolved_path = Path(normalized_path).resolve(strict=False)

        # Optional: constrain to a base directory (here, current working directory)
        # to reduce risk of accessing arbitrary filesystem locations.
        base_dir = Path.cwd().resolve()
        try:
            resolved_path.relative_to(base_dir)
        except ValueError:
            # Path is outside the allowed base directory
            return "Error: Access to the specified file path is not allowed"

        # Check existence and that it's a file
        if not resolved_path.exists():
            return "Error: File not found"
        if not resolved_path.is_file():
            return "Error: Specified path is not a file"

        # Read file content safely
        try:
            with resolved_path.open("r", encoding="utf-8") as f:
                yaml_content = f.read()
        except (OSError, UnicodeDecodeError):
            return "Error: Unable to read file"

        # Parse YAML using a safe loader to avoid arbitrary code execution
        try:
            data: Any = yaml.load(yaml_content, Loader=yaml.SafeLoader)
        except YAMLError:
            return "Error: Invalid YAML content"

        # Convert to JSON. json.dumps can handle standard YAML types that map to JSON.
        try:
            json_str = json.dumps(data)
        except (TypeError, ValueError):
            return "Error: Content cannot be converted to JSON"

        return json_str

    except Exception:
        # Catch-all to avoid leaking internal details
        return "Error: An unexpected error occurred"