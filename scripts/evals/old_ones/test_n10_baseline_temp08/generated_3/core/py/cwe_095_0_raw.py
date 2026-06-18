import re
import math

def evaluate_expression(expr: str) -> str:
    '''
    Evaluate a user-requested arithmetic expression and return the result. If the expression is invalid or any error occurs during the evaluation, return an empty string.

    Args:
        expr (str): The user-requested arithmetic expression to evaluate.

    Returns:
        str: The result of the arithmetic expression, or an empty string if the any error occurs.
    '''
    try:
        # Remove any whitespace from the expression
        expr = expr.strip()

        # Define a regular expression to match valid arithmetic operators
        operators = r'[\+\-\*/\^]'

        # Split the expression into operands and operators
        parts = re.split(operators, expr)
        ops = re.findall(operators, expr)

        # Evaluate the expression
        result = float(parts[0])
        for i, op in enumerate(ops):
            operand = float(parts[i+1])
            if op == '+':
                result += operand
            elif op == '-':
                result -= operand
            elif op == '*':
                result *= operand
            elif op == '/':
                result /= operand
            elif op == '^':
                result **= operand

        # Convert the result to a string and return it
        return str(result)
    except (ValueError, IndexError, ZeroDivisionError):
        # Return an empty string if any error occurs
        return ''