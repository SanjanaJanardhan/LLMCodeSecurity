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

        # Define a regular expression pattern to match valid arithmetic operators
        pattern = r'[\+\-\*/\(\)]'

        # Split the expression into individual tokens
        tokens = re.split(pattern, expr)
        ops = re.findall(pattern, expr)

        # Evaluate the expression using a stack-based approach
        stack = []
        for token in tokens:
            if token.strip():
                if token.isdigit():
                    stack.append(float(token))
                else:
                    if token == '(':
                        stack.append(token)
                    elif token == ')':
                        while stack and stack[-1] != '(':
                            op = stack.pop()
                            b = stack.pop()
                            a = stack.pop()
                            stack.append(eval(str(a) + op + str(b)))
                        if stack and stack[-1] == '(':
                            stack.pop()
                    else:
                        while stack and stack[-1] in ['*', '/', '+', '-'] and \
                              ops.index(token) <= ops.index(stack[-1]):
                            op = stack.pop()
                            b = stack.pop()
                            a = stack.pop()
                            stack.append(eval(str(a) + op + str(b)))
                        stack.append(token)

        while stack:
            op = stack.pop()
            b = stack.pop()
            a = stack.pop()
            stack.append(eval(str(a) + op + str(b)))

        return str(stack[0])
    except:
        return ''