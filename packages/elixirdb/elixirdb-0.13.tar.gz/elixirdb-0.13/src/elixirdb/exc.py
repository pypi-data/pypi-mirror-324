"Model Validation Errors"

from __future__ import annotations


REF_URL = "https://github.com/hotnsoursoup/quik-db/blob/master/README.md"


def pprint_validation_errors(validation_error):
    """
    Prints validation errors extracted from a ValidationError object
    with linked information.

    Parameters:
    - validation_error: ValidationError object (e.g., from pydantic).
    - databases: Dictionary containing database keys and their names.
    """
    errors = validation_error.errors()  # Extract errors from ValidationError
    messages = []
    error_map = {}
    for error in errors:
        # Extract location and determine database name
        loc = error.get("loc", [])
        if loc and loc[0] == "database" and len(loc) > 1:
            name = loc[1]
        else:
            name = loc[0] if loc else None
        error_map[name] = [*error_map.get(name, []), error]

    for name, error in error_map.items():
        # Extract location and determine database name
        loc = error.get("loc", [])
        # Add database-specific header if name is available
        if name:
            messages.append(f"\n{name} configuration errors:")

        # Extract error link
        if loc and loc[0] == "engines":
            location = ".".join(map(str, loc[1:]))
        else:
            location = ".".join(map(str, loc))

        msg = error.get("msg", "Unknown error message")
        error_type = error.get("type", "Unknown type")

        # Initialize error message
        error_msg = (
            f"  - Location: {location}\n    Message: {msg}\n    Type: {error_type}"
        )

        # Add additional context if present
        for key, value in error.get("ctx", {}).items():
            error_msg += f"\n    {key}: {value}"

        messages.append(error_msg)

    # Print all messages
    for message in messages:
        print(message)


def get_error_msg(error: dict) -> str:
    """
    Extract and return an error message from a given error dictionary.

    Args:
        error (dict): A dictionary containing error information.

    Returns:
        str: The extracted error message. If the "ctx" dictionary
            contains an "error" key, its value is returned. Otherwise,
            the value of the "msg" key in the error dictionary is
            returned. If neither is present, an empty string is returned.

    """
    ctx = error.get("ctx", {})
    if ctx and ctx.get("error"):
        return ctx.pop("error")
    return error.get("msg", "")


class ElixirConfigError(Exception):
    """
    Base exception class for ElixirDB configuration errors.
    """


class InvalidElixirConfigError(ElixirConfigError):
    """Exception raised when an invalid configuration is provided."""


class ElixirFileNotFoundError(ElixirConfigError):
    """Exception raised when a specified configuration name is not found."""


class EngineKeyNotFoundError(ElixirConfigError):
    """Exception raised when a specified configuration name is not found."""

    def __init__(self, engine_key: str, message: str | None = None):
        if not message:
            message = f"Engine key '{engine_key}' not found in the configuration."
        message = message.format(engine_key=engine_key)

        super().__init__(message)


class EngineKeyNotDefinedError(ElixirConfigError):
    """
    Exception raised when a configuration could not be identified because
    an 'engine_key' was not provided or a 'default' configuration could not
    be found.

    :class:'elixirdb.models.manager.Config'
    """


class InvalidEngineTypeError(Exception):
    """
    Exception raised when attempting to create a session factory in
    direct connection mode.
    """
