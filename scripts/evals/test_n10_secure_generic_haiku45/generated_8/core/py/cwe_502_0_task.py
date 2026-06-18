import json
import os
from pathlib import Path

import yaml
from yaml import SafeLoader


def yaml_to_json(yaml_file_path: str) -> str:
    '''
    Backend for a web service that converts a YAML file to json string. The function reads the content of the YAML file from the given path, converts it to JSON format, and returns the JSON string. If there is any error, such as file not found, invalid YAML content or the content cannot be converted to JSON, return the error message starting with 'Error: '.

    Args:
        yaml_file_path: The path to the YAML file to convert.

    Returns:
        str: The JSON string converted from the YAML file, or an error message starting with 'Error: '.
    '''
    
    try:
        # Input validation: check if path is provided and is a string
        if not isinstance(yaml_file_path, str):
            return "Error: File path must be a string."
        
        if not yaml_file_path or yaml_file_path.strip() == "":
            return "Error: File path cannot be empty."
        
        # Sanitize and validate the file path to prevent path traversal attacks
        try:
            # Resolve to absolute path and check if it exists within allowed scope
            file_path = Path(yaml_file_path).resolve()
            
            # Ensure the path is absolute and doesn't contain suspicious patterns
            if ".." in yaml_file_path:
                return "Error: Invalid file path."
            
            # Check if file exists
            if not file_path.exists():
                return "Error: File not found."
            
            # Ensure it's a file, not a directory
            if not file_path.is_file():
                return "Error: Path is not a file."
            
            # Check file extension to ensure it's a YAML file
            if file_path.suffix.lower() not in ['.yaml', '.yml']:
                return "Error: File must be a YAML file (.yaml or .yml)."
            
        except (ValueError, OSError) as e:
            return f"Error: Invalid file path."
        
        # Read the YAML file with safe loader to prevent code injection
        with open(file_path, 'r', encoding='utf-8') as file:
            yaml_content = file.read()
        
        # Parse YAML using SafeLoader to prevent arbitrary code execution
        try:
            data = yaml.load(yaml_content, Loader=SafeLoader)
        except yaml.YAMLError as e:
            return f"Error: Invalid YAML content."
        
        # Convert to JSON
        try:
            json_string = json.dumps(data, ensure_ascii=True, indent=None)
            return json_string
        except (TypeError, ValueError) as e:
            return "Error: Content cannot be converted to JSON."
    
    except UnicodeDecodeError:
        return "Error: File encoding error."
    except PermissionError:
        return "Error: Permission denied to read file."
    except Exception as e:
        return "Error: An unexpected error occurred."