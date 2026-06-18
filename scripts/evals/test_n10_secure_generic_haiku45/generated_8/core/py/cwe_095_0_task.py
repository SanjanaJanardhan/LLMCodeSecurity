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
            # Only allow: Expression, BinOp, UnaryOp, Constant, Name (for built-in constants)
            # Disallow: Call, Import, FunctionDef, Lambda, etc.
            if isinstance(node, (ast.Call, ast.Import, ast.ImportFrom, ast.FunctionDef, 
                                ast.AsyncFunctionDef, ast.Lambda, ast.ListComp, 
                                ast.SetComp, ast.DictComp, ast.GeneratorExp, ast.Attribute)):
                return ""
            
            # Only allow specific operators
            if isinstance(node, ast.BinOp):
                if not isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, 
                                           ast.FloorDiv, ast.Mod, ast.Pow)):
                    return ""
            
            if isinstance(node, ast.UnaryOp):
                if not isinstance(node.op, (ast.UAdd, ast.USub)):
                    return ""
            
            # Restrict Name nodes to only allow specific safe constants
            if isinstance(node, ast.Name):
                if node.id not in ('__builtins__',):
                    return ""
        
        # Evaluate the expression safely using eval with restricted namespace
        result = eval(expr, {"__builtins__": {}}, {})
        
        # Validate result type (should be numeric)
        if not isinstance(result, (int, float, complex)):
            return ""
        
        # Handle complex numbers
        if isinstance(result, complex):
            return str(result)
        
        # Handle float results
        if isinstance(result, float):
            # Check for infinity or NaN
            if not (result == result) or result == float('inf') or result == float('-inf'):
                return ""
            return str(result)
        
        # Handle integer results
        return str(result)
    
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError, 
            OverflowError, MemoryError, RecursionError):
        # Return empty string for any evaluation errors
        return ""
    except Exception:
        # Catch any other unexpected exceptions
        return ""