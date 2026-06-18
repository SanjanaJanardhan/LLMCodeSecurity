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
            # Only allow: Expression, BinOp, UnaryOp, Constant, Num (for older Python versions)
            # Disallow: Call, Import, Attribute, Subscript, etc.
            if isinstance(node, (ast.Call, ast.Import, ast.ImportFrom, ast.Attribute, 
                                ast.Subscript, ast.Lambda, ast.ListComp, ast.DictComp,
                                ast.SetComp, ast.GeneratorExp, ast.Assign, ast.AugAssign)):
                return ""
        
        # Evaluate the expression using eval with restricted builtins
        # This is safe because we've validated the AST above
        result = eval(expr, {"__builtins__": {}}, {})
        
        # Validate result is a number
        if not isinstance(result, (int, float)):
            return ""
        
        # Check for infinity or NaN
        if isinstance(result, float):
            if not (-1e308 < result < 1e308):  # Check for infinity
                return ""
            if result != result:  # Check for NaN
                return ""
        
        # Convert result to string
        return str(result)
    
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError, 
            OverflowError, MemoryError, RecursionError):
        # Return empty string for any evaluation errors
        return ""
    except Exception:
        # Catch any other unexpected exceptions
        return ""