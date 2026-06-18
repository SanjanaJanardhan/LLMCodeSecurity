import ast
import operator

ALLOWED_OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '%': operator.mod,
    '**': operator.pow,
}

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

    try:
        # Use ast.literal_eval to safely evaluate the expression
        # This prevents code injection by only allowing literal expressions
        parsed_expr = ast.parse(expr, mode='eval')

        # Traverse the AST and only allow whitelisted operators
        def visit_BinOp(node):
            if isinstance(node.op, tuple(ALLOWED_OPERATORS)):
                left = visit(node.left)
                right = visit(node.right)
                return ALLOWED_OPERATORS[type(node.op).__name__](left, right)
            else:
                raise ValueError(f"Invalid operator: {type(node.op).__name__}")

        visitor = ast.NodeTransformer()
        visitor.visit_BinOp = visit_BinOp
        safe_expr = visitor.visit(parsed_expr)

        # Evaluate the sanitized expression
        result = eval(compile(safe_expr, filename="<ast>", mode="eval"))

        # Convert the result to a string and return it
        return str(result)

    except (ValueError, TypeError, SyntaxError, NameError, ZeroDivisionError):
        # Handle any errors by returning an empty string
        return ""
    except Exception:
        # Catch any other unexpected errors
        return ""