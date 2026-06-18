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
        
        # Resolve the path to prevent path traversal attacks
        try:
            resolved_path = Path(yaml_file_path).resolve()
        except (ValueError, RuntimeError) as e:
            return f"Error: Invalid file path: {str(e)}"
        
        # Verify the file exists and is a file (not a directory)
        if not resolved_path.exists():
            return "Error: File not found."
        
        if not resolved_path.is_file():
            return "Error: Path is not a file."
        
        # Check file extension to ensure it's a YAML file
        if resolved_path.suffix.lower() not in ['.yaml', '.yml']:
            return "Error: File must have .yaml or .yml extension."
        
        # Read the file with size limit to prevent DoS attacks
        max_file_size = 10 * 1024 * 1024  # 10 MB limit
        file_size = resolved_path.stat().st_size
        
        if file_size > max_file_size:
            return "Error: File size exceeds maximum allowed size."
        
        # Read the YAML file
        with open(resolved_path, 'r', encoding='utf-8') as file:
            yaml_content = file.read()
        
        # Parse YAML using SafeLoader to prevent arbitrary code execution
        # SafeLoader is more secure than Loader as it doesn't allow arbitrary Python object instantiation
        parsed_data = yaml.load(yaml_content, Loader=SafeLoader)
        
        # Convert to JSON string
        json_string = json.dumps(parsed_data, ensure_ascii=True, indent=None)
        
        return json_string
    
    except yaml.YAMLError as e:
        return f"Error: Invalid YAML content: {str(e)}"
    except json.JSONDecodeError as e:
        return f"Error: Cannot convert to JSON: {str(e)}"
    except UnicodeDecodeError as e:
        return f"Error: File encoding error: {str(e)}"
    except PermissionError:
        return "Error: Permission denied to read the file."
    except OSError as e:
        return f"Error: File system error: {str(e)}"
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"