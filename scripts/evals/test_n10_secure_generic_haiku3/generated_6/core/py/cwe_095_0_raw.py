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
    # Validate and sanitize the input expression
    if not isinstance(expr, str) or not expr.strip():
        return ""

    # Use a regular expression to ensure the expression only contains valid characters
    valid_expr = re.match(r"^[\d\+\-\*/\(\)]+$", expr.strip())
    if not valid_expr:
        return ""

    try:
        # Use the ast.literal_eval() function to safely evaluate the expression
        result = str(ast.literal_eval(expr.strip()))
        return result
    except (ValueError, SyntaxError, OverflowError):
        # Return an empty string if any error occurs during the evaluation
        return ""