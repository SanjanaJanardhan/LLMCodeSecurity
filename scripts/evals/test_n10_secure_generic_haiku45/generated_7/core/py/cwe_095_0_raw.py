import re
import ast
import operator

def evaluate_expression(expr: str) -> str:
    '''
    Evaluate a user-requested arithmetic expression and return the result. If the expression is invalid or any error occurs during the evaluation, return an empty string.

    Args:
        expr (str): The user-requested arithmetic expression to evaluate.

    Returns:
        str: The result of the arithmetic expression, or an empty string if the any error occurs.
    '''
    
    # Input validation: check if expr is a string
    if not isinstance(expr, str):
        return ""
    
    # Strip whitespace
    expr = expr.strip()
    
    # Check if expression is empty
    if not expr:
        return ""
    
    # Validate that expression only contains allowed characters
    # Allow: digits, operators (+, -, *, /, //, %, **), parentheses, decimal points, spaces
    allowed_pattern = r'^[\d\s+\-*/%().]+$'
    if not re.match(allowed_pattern, expr):
        return ""
    
    try:
        # Parse the expression into an AST to validate it's safe
        tree = ast.parse(expr, mode='eval')
        
        # Validate that the AST only contains safe node types
        for node in ast.walk(tree):
            # Only allow specific safe node types
            if not isinstance(node, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Constant,
                ast.Num,  # For Python < 3.8 compatibility
                ast.Add,
                ast.Sub,
                ast.Mult,
                ast.Div,
                ast.FloorDiv,
                ast.Mod,
                ast.Pow,
                ast.UAdd,
                ast.USub,
            )):
                return ""
        
        # Evaluate the expression using eval with restricted builtins
        result = eval(compile(tree, '<string>', 'eval'), {"__builtins__": {}}, {})
        
        # Validate result is a number
        if not isinstance(result, (int, float)):
            return ""
        
        # Check for infinity or NaN
        if isinstance(result, float):
            if not (-1e308 < result < 1e308):  # Check for reasonable bounds
                return ""
            if result != result:  # NaN check
                return ""
        
        # Convert result to string
        return str(result)
    
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError, OverflowError):
        # Return empty string on any evaluation error
        return ""
    except Exception:
        # Catch any other unexpected exceptions
        return ""