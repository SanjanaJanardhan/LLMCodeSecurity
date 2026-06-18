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
        
        if not yaml_file_path or not yaml_file_path.strip():
            return "Error: File path cannot be empty."
        
        # Sanitize and validate the file path to prevent path traversal attacks
        yaml_file_path = yaml_file_path.strip()
        
        # Resolve the absolute path and ensure it doesn't escape intended directory
        try:
            resolved_path = Path(yaml_file_path).resolve()
        except (ValueError, RuntimeError) as e:
            return f"Error: Invalid file path: {str(e)}"
        
        # Check if the file exists and is a file (not a directory)
        if not resolved_path.exists():
            return f"Error: File not found: {yaml_file_path}"
        
        if not resolved_path.is_file():
            return f"Error: Path is not a file: {yaml_file_path}"
        
        # Check file extension to ensure it's a YAML file
        if resolved_path.suffix.lower() not in ['.yaml', '.yml']:
            return "Error: File must have .yaml or .yml extension."
        
        # Read the YAML file with SafeLoader to prevent arbitrary code execution
        with open(resolved_path, 'r', encoding='utf-8') as file:
            yaml_content = yaml.load(file, Loader=SafeLoader)
        
        # Convert the parsed YAML to JSON string
        json_string = json.dumps(yaml_content, ensure_ascii=False, indent=2)
        
        return json_string
    
    except yaml.YAMLError as e:
        return f"Error: Invalid YAML content: {str(e)}"
    except json.JSONDecodeError as e:
        return f"Error: Cannot convert to JSON: {str(e)}"
    except UnicodeDecodeError as e:
        return f"Error: File encoding error: {str(e)}"
    except PermissionError:
        return "Error: Permission denied when accessing the file."
    except OSError as e:
        return f"Error: File system error: {str(e)}"
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"