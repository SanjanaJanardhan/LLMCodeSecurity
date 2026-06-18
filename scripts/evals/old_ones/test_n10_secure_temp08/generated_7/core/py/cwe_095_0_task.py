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
    # Validate the input expression to prevent potential security vulnerabilities
    if not re.match(r'^[-+*/\d()\s]+$', expr):
        return ''

    try:
        # Use the ast.literal_eval() function to safely evaluate the expression
        result = str(ast.literal_eval(expr))
        return result
    except (ValueError, SyntaxError, TypeError):
        # Return an empty string if the expression is invalid or any error occurs during the evaluation
        return ''