import json

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
    try:
        # Input validation and sanitization
        if not yaml_file_path or not isinstance(yaml_file_path, str):
            return "Error: Invalid YAML file path"

        # Normalize and resolve the path to prevent path traversal attacks
        normalized_path = os.path.normpath(yaml_file_path)
        resolved_path = os.path.realpath(normalized_path)

        # Check if the file exists
        if not os.path.exists(resolved_path):
            return f"Error: YAML file not found at {yaml_file_path}"

        # Read the YAML file content
        with open(resolved_path, 'r') as file:
            yaml_content = file.read()

        # Convert YAML to JSON
        json_content = json.dumps(yaml.load(yaml_content, Loader=Loader))

        return json_content
    except (yaml.YAMLError, json.JSONDecodeError, OSError, ValueError) as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: Unexpected error occurred: {str(e)}"