import re
import ast

def evaluate_expression(expr: str) -> str:
    '''
    Evaluate a user-requested arithmetic expression and return the result. If the expression is invalid or any error occurs during the evaluation, return an empty string.

    Args:
        expr (str): The user-requested arithmetic expression to evaluate.

    Returns:
        str: The result of the arithmetic expression, or an empty string if the any error occurs.
    '''
    # Input validation and sanitization
    if not expr or not isinstance(expr, str):
        return ""

    # Remove any null bytes that could be used for injection
    expr = expr.replace('\0', '')

    # Use a regular expression to validate the expression
    # Only allow basic arithmetic operations (+, -, *, /) and numbers
    if not re.match(r'^[\d\+\-\*\/\s]+$', expr):
        return ""

    try:
        # Use the ast.literal_eval() function to safely evaluate the expression
        # This prevents code injection attacks by only allowing literal expressions
        result = str(ast.literal_eval(expr))
        return result
    except (ValueError, SyntaxError, NameError, TypeError):
        # Handle any errors by returning an empty string
        return ""