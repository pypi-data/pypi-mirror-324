"Wrapper functions for decorators."

import warnings


def deprecated(reason: str):
    """
    A decorator to mark functions as deprecated.
    Args:
        reason (str): The reason why the function is deprecated.
    Returns:
        function: The decorated function that will issue a deprecation
            warning when called.
    Example:
        @deprecated("Use new_function instead.")
        def old_function():
            pass
    """

    def decorator(func):
        def wrapped(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated: {reason}",
                DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        wrapped.__doc__ = f"DEPRECATED: {reason}\n\n" + (func.__doc__ or "")
        return wrapped

    return decorator
