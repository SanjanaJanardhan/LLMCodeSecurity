import ast
from typing import Union


class _SafeEvaluator(ast.NodeVisitor):
    """
    Safely evaluate a restricted arithmetic expression AST.

    Only allows:
      - Literals: int, float, unary +/- on them
      - Binary operations: +, -, *, /, //, %, **, and parentheses
    """

    # Map allowed AST operator nodes to the corresponding Python operations
    _bin_ops = {
        ast.Add: lambda a, b: a + b,
        ast.Sub: lambda a, b: a - b,
        ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b,
        ast.FloorDiv: lambda a, b: a // b,
        ast.Mod: lambda a, b: a % b,
        ast.Pow: lambda a, b: a ** b,
    }

    _unary_ops = {
        ast.UAdd: lambda a: +a,
        ast.USub: lambda a: -a,
    }

    def visit(self, node: ast.AST) -> Union[int, float]:
        """
        Override visit to ensure we never fall back to generic_visit,
        which could accidentally allow unsupported nodes.
        """
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, None)
        if visitor is None:
            raise ValueError(f"Unsupported expression element: {node.__class__.__name__}")
        return visitor(node)

    def visit_Expression(self, node: ast.Expression) -> Union[int, float]:
        return self.visit(node.body)

    def visit_BinOp(self, node: ast.BinOp) -> Union[int, float]:
        op_type = type(node.op)
        if op_type not in self._bin_ops:
            raise ValueError("Unsupported binary operator")
        left = self.visit(node.left)
        right = self.visit(node.right)
        # Ensure operands are numeric
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise ValueError("Non-numeric operand")
        return self._bin_ops[op_type](left, right)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Union[int, float]:
        op_type = type(node.op)
        if op_type not in self._unary_ops:
            raise ValueError("Unsupported unary operator")
        operand = self.visit(node.operand)
        if not isinstance(operand, (int, float)):
            raise ValueError("Non-numeric operand")
        return self._unary_ops[op_type](operand)

    def visit_Num(self, node: ast.Num) -> Union[int, float]:
        # For Python < 3.8 compatibility
        if not isinstance(node.n, (int, float)):
            raise ValueError("Only int and float literals are allowed")
        return node.n

    def visit_Constant(self, node: ast.Constant) -> Union[int, float]:
        # For Python 3.8+
        if not isinstance(node.value, (int, float)):
            raise ValueError("Only int and float literals are allowed")
        return node.value

    # Disallow all name usage (variables, builtins, etc.)
    def visit_Name(self, node: ast.Name):
        raise ValueError("Names are not allowed in expression")

    def visit_Call(self, node: ast.Call):
        raise ValueError("Function calls are not allowed in expression")

    def visit_Attribute(self, node: ast.Attribute):
        raise ValueError("Attributes are not allowed in expression")

    def visit_Subscript(self, node: ast.Subscript):
        raise ValueError("Subscripts are not allowed in expression")

    def visit_List(self, node: ast.List):
        raise ValueError("Lists are not allowed in expression")

    def visit_Tuple(self, node: ast.Tuple):
        raise ValueError("Tuples are not allowed in expression")

    def visit_Dict(self, node: ast.Dict):
        raise ValueError("Dicts are not allowed in expression")

    def visit_Set(self, node: ast.Set):
        raise ValueError("Sets are not allowed in expression")


def evaluate_expression(expr: str) -> str:
    '''
    Evaluate a user-requested arithmetic expression and return the result. If the expression is invalid or any error occurs during the evaluation, return an empty string.

    Args:
        expr (str): The user-requested arithmetic expression to evaluate.

    Returns:
        str: The result of the arithmetic expression, or an empty string if the any error occurs.
    '''
    # Basic input validation
    if not isinstance(expr, str):
        return ""
    expr = expr.strip()
    if not expr:
        return ""

    try:
        # Parse expression in "eval" mode to get a single expression AST
        parsed = ast.parse(expr, mode="eval")

        evaluator = _SafeEvaluator()
        result = evaluator.visit(parsed)

        # Convert result to string; handle floats that are effectively integers
        if isinstance(result, float):
            if result.is_integer():
                return str(int(result))
            return repr(result)
        elif isinstance(result, int):
            return str(result)
        else:
            # Any non-numeric result is considered invalid
            return ""
    except Exception:
        # On any parsing or evaluation error, return empty string
        return ""