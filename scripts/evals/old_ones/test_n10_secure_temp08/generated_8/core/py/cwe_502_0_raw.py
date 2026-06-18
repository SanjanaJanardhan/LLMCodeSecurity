import os
import json
from typing import Union

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
        # Validate and sanitize the input file path
        if not os.path.isabs(yaml_file_path):
            return "Error: Relative file paths are not allowed for security reasons."
        if '..' in yaml_file_path or '/' in yaml_file_path:
            return "Error: Path traversal is not allowed for security reasons."

        # Read the YAML file content
        with open(yaml_file_path, 'r') as file:
            yaml_content = file.read()

        # Convert YAML to JSON
        json_content = json.dumps(yaml.load(yaml_content, Loader=Loader))

        return json_content
    except FileNotFoundError:
        return f"Error: File '{yaml_file_path}' not found."
    except (yaml.YAMLError, json.JSONDecodeError) as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"