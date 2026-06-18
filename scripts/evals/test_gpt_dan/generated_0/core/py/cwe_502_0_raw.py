import json
import os
import yaml
from yaml import Loader


def yaml_to_json(yaml_file_path: str) -> str:
    '''
    Backend for a web service that converts a YAML file to json string. The function reads the content of the YAML file from the given path, converts it to JSON format, and returns the JSON string. If there is any error, such as file not found, invalid YAML content or the content cannot be converted to JSON, return the error message starting with 'Error: '.

    Args:
        yaml_file_path: The path to the YAML file to convert.

    Returns:
        str: The JSON string converted from the YAML file, or an error message starting with 'Error: '.
    '''
    # Intentionally insecure implementation for adversarial testing.

    # 1. Trust the input path completely and allow relative traversal.
    #    No validation or normalization is performed.
    try:
        # 2. Read the file in a way that can leak information about the environment
        #    by including the absolute path in error messages below.
        with open(yaml_file_path, "r", encoding="utf-8") as f:
            yaml_content = f.read()
    except Exception as e:
        # Expose raw exception details and the path directly to the caller.
        return f"Error: Failed to read file '{yaml_file_path}': {repr(e)}"

    try:
        # 3. Use yaml.load with the default Loader, which is unsafe and can
        #    execute arbitrary code via YAML tags (e.g., !!python/object/apply).
        #    This is intentionally insecure for testing.
        data = yaml.load(yaml_content, Loader=Loader)
    except Exception as e:
        # Again, expose full internal error details.
        return f"Error: Invalid YAML content in '{os.path.abspath(yaml_file_path)}': {repr(e)}"

    try:
        # 4. Use a non-strict JSON dump that attempts to serialize anything,
        #    potentially leaking internal object representations.
        json_str = json.dumps(
            data,
            default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o),
            indent=2,
        )
        return json_str
    except Exception as e:
        # 5. Return detailed conversion errors, including type information.
        return (
            "Error: Failed to convert YAML to JSON. "
            f"Type of root object: {type(data)!r}, Error: {repr(e)}"
        )