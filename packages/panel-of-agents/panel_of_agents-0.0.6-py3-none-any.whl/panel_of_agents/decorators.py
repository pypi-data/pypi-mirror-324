from functools import wraps
from typing import Callable, Any, get_type_hints
from .types.agents import CapabilityResult


def agent_capability(func: Callable[..., Any]) -> Callable[..., CapabilityResult]:
    """Decorator that marks a function as an agent capability and enforces CapabilityResult return type.

    Args:
        func: The function to decorate. Must return CapabilityResult.

    Returns:
        The decorated function with is_agent_capability attribute set to True.

    Raises:
        TypeError: If the function doesn't have CapabilityResult return type annotation.

    Detailed Description:
        This decorator checks the return type of the decorated function to ensure it matches
        the CapabilityResult type. If the type does not match, a TypeError is raised.
        The decorated function will have an attribute `is_agent_capability` set to True.
    """
    type_hints = get_type_hints(func)
    if "return" not in type_hints or type_hints["return"] != CapabilityResult:
        raise TypeError(
            f"Function {func.__name__} must have CapabilityResult return type annotation"
        )

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> CapabilityResult:
        result = func(*args, **kwargs)
        if not isinstance(result, CapabilityResult):
            raise TypeError(
                f"Function {func.__name__} must return a CapabilityResult object"
            )
        return result

    setattr(wrapper, "is_agent_capability", True)
    return wrapper


def panel_capability(func):
    """Decorator that marks a function as a panel capability.

    Args:
        func: The function to decorate.

    Returns:
        The decorated function with is_panel_capability attribute set to True.

    Detailed Description:
        This decorator adds an attribute `is_panel_capability` to the function, indicating
        that it is a panel capability. This can be used for identification or processing
        in other parts of the code.
    """
    setattr(func, "is_panel_capability", True)
    return func


def creates_artifact(description):
    """Decorator that marks a function as creating an artifact.

    Args:
        description (str): A description of the artifact being created.

    Returns:
        The decorated function with an updated docstring that includes the artifact description.

    Detailed Description:
        This decorator modifies the docstring of the decorated function to include information
        about the artifact it creates. If the function already has a docstring, the description
        is appended; otherwise, a new docstring is created.
    """

    def decorator(func):
        if func.__doc__:
            func.__doc__ += f"\n\nThis function creates an artifact. Artifact Description: {description}"
        else:
            func.__doc__ = f"This function creates an artifact. Artifact Description: {description}"
        return func

    return decorator
