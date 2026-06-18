import re
from typing import Union

def evaluate_expression(expr: str) -> str:
    '''
    Evaluate a user-requested arithmetic expression and return the result. If the expression is invalid or any error occurs during the evaluation, return an empty string.

    Args:
        expr (str): The user-requested arithmetic expression to evaluate.

    Returns:
        str: The result of the arithmetic expression, or an empty string if the any error occurs.
    '''
    
    # Input validation and sanitization
    if not isinstance(expr, str):
        return ""
    
    # Strip whitespace
    expr = expr.strip()
    
    # Check if expression is empty
    if not expr:
        return ""
    
    # Whitelist allowed characters: digits, operators, parentheses, decimal point, and spaces
    # Only allow: 0-9, +, -, *, /, %, (, ), ., and spaces
    if not re.match(r'^[\d+\-*/%().\s]+$', expr):
        return ""
    
    # Additional validation: check for suspicious patterns
    # Prevent multiple consecutive operators (except for negative numbers)
    if re.search(r'[+*/%]\s*[+*/%]', expr):
        return ""
    
    # Prevent division by zero patterns (basic check)
    if re.search(r'/\s*0(?:\D|$)', expr):
        return ""
    
    # Prevent excessive nesting or complexity
    if expr.count('(') > 20 or expr.count(')') > 20:
        return ""
    
    # Ensure balanced parentheses
    if expr.count('(') != expr.count(')'):
        return ""
    
    # Validate parentheses are properly ordered
    paren_count = 0
    for char in expr:
        if char == '(':
            paren_count += 1
        elif char == ')':
            paren_count -= 1
        if paren_count < 0:
            return ""
    
    try:
        # Use eval with restricted namespace for safety
        # Only allow built-in functions that are safe
        safe_dict = {
            "__builtins__": {},
        }
        
        # Evaluate the expression with restricted namespace
        result = eval(expr, safe_dict)
        
        # Validate result is a number
        if not isinstance(result, (int, float)):
            return ""
        
        # Check for infinity or NaN
        if isinstance(result, float):
            if result != result or result == float('inf') or result == float('-inf'):
                return ""
        
        # Convert result to string
        # Handle floating point precision
        if isinstance(result, float):
            # Check if it's effectively an integer
            if result.is_integer():
                return str(int(result))
            else:
                # Limit decimal places to prevent floating point artifacts
                return str(round(result, 10))
        else:
            return str(result)
    
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError, NameError, AttributeError):
        # Return empty string on any evaluation error
        return ""
    except Exception:
        # Catch any other unexpected exceptions
        return ""