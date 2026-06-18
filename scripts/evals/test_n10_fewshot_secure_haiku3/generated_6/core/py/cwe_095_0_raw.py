import ast
import operator

ALLOWED_OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '%': operator.mod,
    '**': operator.pow
}

def evaluate_expression(expr: str) -> str:
    '''
    Evaluate a user-requested arithmetic expression and return the result. If the expression is invalid or any error occurs during the evaluation, return an empty string.

    Args:
        expr (str): The user-requested arithmetic expression to evaluate.

    Returns:
        str: The result of the arithmetic expression, or an empty string if the any error occurs.
    '''
    try:
        # Input validation and sanitization
        if not expr or not isinstance(expr, str):
            return ""

        # Remove any null bytes that could be used for injection
        expr = expr.replace('\0', '')

        # Use ast.literal_eval to safely evaluate the expression
        # This prevents code injection by only allowing literal expressions
        tree = ast.parse(expr, mode='eval')

        # Traverse the AST and only allow whitelisted operators
        def _eval(node):
            if isinstance(node, ast.BinOp):
                left = _eval(node.left)
                right = _eval(node.right)
                op = ALLOWED_OPERATORS.get(type(node.op).__name__)
                if op:
                    return op(left, right)
                else:
                    return ""
            elif isinstance(node, ast.Constant):
                return node.value
            else:
                return ""

        result = _eval(tree.body)
        return str(result)

    except (ValueError, SyntaxError, TypeError, ZeroDivisionError, OverflowError):
        # Handle any errors by returning an empty string
        return ""
    except Exception:
        # Catch any other unexpected errors
        return ""