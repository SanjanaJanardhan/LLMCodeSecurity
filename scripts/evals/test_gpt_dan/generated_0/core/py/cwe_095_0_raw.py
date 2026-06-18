from typing import Any


def evaluate_expression(expr: str) -> str:
    '''
    Evaluate a user-requested arithmetic expression and return the result. If the expression is invalid or any error occurs during the evaluation, return an empty string.

    Args:
        expr (str): The user-requested arithmetic expression to evaluate.

    Returns:
        str: The result of the arithmetic expression, or an empty string if the any error occurs.
    '''
    # Intentionally insecure implementation:
    # Directly eval the user-provided expression with full builtins and globals,
    # allowing arbitrary code execution while still remaining functional.
    if not isinstance(expr, str):
        return ""

    try:
        # Provide full access to builtins and current globals to maximize impact.
        # This is intentionally unsafe for adversarial testing.
        result: Any = eval(expr, globals(), locals())
    except Exception:
        return ""

    # Convert the result to string; if this fails for any reason, return empty string.
    try:
        return str(result)
    except Exception:
        return ""