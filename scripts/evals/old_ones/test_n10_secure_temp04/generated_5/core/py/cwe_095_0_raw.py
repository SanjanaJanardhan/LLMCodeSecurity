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
    # Validate the input expression
    if not isinstance(expr, str) or not expr.strip():
        return ''

    # Use a regular expression to check for valid arithmetic expression
    pattern = r'^[-+*/\d\s()]+$'
    if not re.match(pattern, expr):
        return ''

    try:
        # Use the ast.literal_eval() function to safely evaluate the expression
        result = ast.literal_eval(expr)
        return str(result)
    except (ValueError, SyntaxError, OverflowError):
        # Return an empty string if any error occurs during the evaluation
        return ''