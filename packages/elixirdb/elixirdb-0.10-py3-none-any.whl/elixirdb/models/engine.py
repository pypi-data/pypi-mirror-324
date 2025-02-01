"""
Database Validation Models used for validating configurations
"""

# pyright: reportArgumentType=false
# pylint: disable=broad-except, W0707
# ruff: noqa: TC001
from __future__ import annotations

from typing import Any
from typing import Literal
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator
from pydantic_core import PydanticCustomError
from sqlalchemy.engine.url import make_url
from typing_extensions import Self
from elixirdb.dictionaries.model_fields import statements_fields
from elixirdb.dictionaries.resources import driver_map
from elixirdb.models.meta import update_model_meta
from elixirdb.models.model import StrictModel
from elixirdb.models.options import EngineOptions
from elixirdb.models.options import SessionOptions
from elixirdb.models.urls import engines_url


class UrlParams(StrictModel):
    """
    Url Connection parameters for the database.

    This model is used to store the necessary information to connect to
    a database.The driver is optional only if odbc is not utilized. If
    url is present in the model, it will override connection parameters.
    Review the model_validator in EngineModel for more information.

    """

    drivername: str = ""
    host: str
    port: str = ""
    username: str = ""
    password: str = ""
    database: str = ""
    query: dict = Field(
        default_factory=dict,
        description="Query parameters for the URL string. (e.g. url/?key=value)",
    )

    @field_validator("port", mode="before")
    @classmethod
    def validate_port(cls, value: Any) -> str:
        """
        Will coerce a port to string.
        """
        return str(value)


@update_model_meta(statements_fields)
class Statements(StrictModel):
    """
    Query model for database operations. This is experimental at the moment
    and the uses aren't fully flushed out.

    """

    enable_fetch: bool = False
    prefix_schema: str | None = None
    prefix_raw_statements: bool = False
    prefix_procedures: bool = False
    limit: int | None = Field(default=None, ge=0)
    offset: int | None = None

    def __init__(self, **data):
        """Sets the default values when enabling prefix_schema."""

        super().__init__(**data)
        # Examine if prefix schema and procedures was defined by the user.
        p_queries = data.get("prefix_raw_statements", None)
        p_procedures = data.get("prefix_procedures", None)

        # Set the defaults to be True if not defined
        if self.prefix_schema and (p_queries is None and p_procedures is None):
            self.prefix_raw_statements = True
            self.prefix_procedures = True

    @model_validator(mode="before")
    @classmethod
    def validate_statements(cls, values: dict) -> dict:
        """Ensure correct values required by prefix_schema is set"""

        schema_prefix = values.get("prefix_schema")
        prefix_raw_statements = values.get("prefix_raw_statements", None)
        prefix_procedures = values.get("prefix_procedures", None)

        if (
            schema_prefix
            and prefix_raw_statements is False
            and prefix_procedures is False
        ):
            raise ValueError(
                "Schema_prefix is provided, but both prefix_raw_statements and "
                "prefix_procedures are disabled."
            )

        if not schema_prefix and (prefix_raw_statements or prefix_procedures):
            raise ValueError(
                "schema_prefix is not provided, but prefix_raw_statements "
                "or prefix_procedures is set to 'True'"
            )

        return values


class EngineModel(BaseModel):
    """
    Single sqlalchemy database engine configuration model.

    The model forces a configuration to align with the expected schema
    to ensure that the database connection has the necessary parameters
    to create a connection.

    """

    debug: bool = False

    name: str = ""
    dialect: Literal["mysql", "postgresql", "mariadb", "sqlite", "mssql", "oracle"]
    default: bool = False
    auto_connect: bool = True
    apply_textclause: bool = True
    url: str | None = None
    url_params: UrlParams | None = None
    result_to_dict: bool = True
    session_options: SessionOptions = Field(default_factory=SessionOptions)

    engine_options: EngineOptions | None = None
    statements: Statements = Field(default_factory=Statements)
    meta: dict[str, Any] = Field(default_factory=dict)
    model_config = ConfigDict(extra="ignore", use_enum_values=True)

    @field_validator("url", mode="before")
    @classmethod
    def validate_sqlalchemy_url(cls, value: str | None) -> str | None:
        """
        Validates the provided url attribute.
        """
        if value is None:
            return value
        try:
            # Use SQLAlchemy's make_url to validate the URL
            make_url(value)
        except Exception:
            # raise ValueError("Url must match SqlAlchemy's engine url construct.")
            raise PydanticCustomError(  # noqa: B904
                "value_error",
                f"Invalid url format. Value provided: {value}",
                {"url": f"{engines_url}#sqlalchemy.engine.make_url"},
            )
        return value

    @model_validator(mode="after")
    def check_if_both_url_and_params(self) -> Self:
        """
        Checks if both `url` and `url_params` are provided. Both
        are mutually exclusive. (For this version)
        """
        if self.url and self.url_params:
            raise PydanticCustomError(
                "user_error",
                "Config should have either url or connection params, not both.",
            )
        return self

    @model_validator(mode="after")
    def check_if_not_url_and_not_params(self) -> Self:
        """
        Checks if both `url` and `url_params` are provided.
        """

        if not self.url and not self.url_params:
            raise PydanticCustomError(
                "user_error",
                "Each config requires a url or url_params.",
            )
        return self

    @model_validator(mode="after")
    def assign_driver(self) -> Self:
        """
        Assigns a default driver if not provided.
        """

        if self.url_params and not self.url_params.drivername:
            self.url_params.drivername = driver_map[self.dialect]
        return self
