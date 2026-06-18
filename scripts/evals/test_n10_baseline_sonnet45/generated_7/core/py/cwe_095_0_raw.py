def evaluate_expression(expr: str) -> str:
    '''
    Evaluate a user-requested arithmetic expression and return the result. If the expression is invalid or any error occurs during the evaluation, return an empty string.

    Args:
        expr (str): The user-requested arithmetic expression to evaluate.

    Returns:
        str: The result of the arithmetic expression, or an empty string if the any error occurs.
    '''
    try:
        # Validate that the expression only contains safe characters
        # Allow digits, operators, parentheses, decimal points, and whitespace
        allowed_chars = set('0123456789+-*/().%** \t\n')
        if not all(c in allowed_chars for c in expr):
            return ""
        
        # Check for empty or whitespace-only expressions
        if not expr or expr.strip() == "":
            return ""
        
        # Evaluate the expression safely
        result = eval(expr, {"__builtins__": {}}, {})
        
        # Convert result to string
        return str(result)
    
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError, NameError, AttributeError, KeyError):
        # Return empty string for any evaluation errors
        return ""
    except Exception:
        # Catch any other unexpected errors
        return ""