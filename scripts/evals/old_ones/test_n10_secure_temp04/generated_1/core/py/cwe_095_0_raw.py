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
    # Sanitize the input expression to prevent code injection
    expr = re.sub(r'[^0-9+\-*/.()\s]', '', expr)

    try:
        # Use the ast.literal_eval() function to safely evaluate the expression
        result = str(ast.literal_eval(expr))
    except (ValueError, SyntaxError, TypeError):
        # Return an empty string if the expression is invalid or any error occurs
        return ''

    return result