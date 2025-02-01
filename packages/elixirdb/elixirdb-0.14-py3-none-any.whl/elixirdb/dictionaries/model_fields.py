"""
Collection of dictionaries used to store messages related to database models,
configuration, and errors.
"""

# flake8: noqa: E501

url_params_fields = {
    "drivername": {
        "title": "Database Driver",
        "description": (
            "Specifies the driver for the database connection, which may vary "
            "across database dialects or when ODBC support is enabled."
        ),
        "example": "mysql+pymysql",
    },
    "host": {
        "title": "Database Host",
        "description": "The hostname or IP address of the database server.",
        "example": "127.0.0.1",
    },
    "port": {
        "title": "Database Port",
        "description": "The port number that the database server is listening on.",
        "example": 5432,
    },
    "username": {
        "title": "Database Username",
        "description": "The username for authenticating the database connection.",
        "example": "user123",
    },
    "password": {
        "title": "Database Password",
        "description": "The password associated with the database username.",
        "example": "pass123",
    },
    "database": {
        "title": "Database Name",
        "description": "The name of the specific database to connect to.",
        "example": "mydatabase",
    },
    "query": {
        "title": "URL Query Parameters",
        "description": (
            "Optional query parameters to include in the connection URL, "
            "formatted as key-value pairs (e.g., ?param1=value1&param2=value2)."
        ),
        "example": {"param1": "value1", "param2": "value2"},
    },
}

# url_params_fields = flatten_dict(url_params_fields)

statements_fields = {
    "enable_fetch": {
        "title": "Enable Fetch",
        "description": (
            "Enabled by default. Fetches results from the Result object. "
            "Set to False to disable fetching and return the Result object."
        ),
    },
    "prefix_schema": {
        "title": "Schema Prefix",
        "description": (
            "The prefix format to add to query names, stored procedures, "
            "or functions if they do not already have a schema prefix."
        ),
    },
    "prefix_raw_statements": {
        "title": "Prefix Queries",
        "description": "If set to True, applies the schema prefix to queries.",
    },
    "prefix_procedures": {
        "title": "Prefix Procedures",
        "description": (
            "If set to True, applies the schema prefix to stored procedures "
            "or function names."
        ),
    },
    "limit": {
        "title": "limit",
        "description": (
            "Limits the number of rows returned in raw queries, implementing "
            "paging. Setting this to 0 disables paging."
        ),
    },
    "offset": {
        "title": "offset",
        "description": (
            "Specifies the number of rows to skip before returning results. "
            "This is useful for implementing paging across all queries."
        ),
    },
}

# statements_fields = flatten_dict(statements_fields)

db_model_fields = {
    "name": {
        "title": "The reference name for the database.",
        "description": "The name of the database being connected to.",
        "example": "mydatabase",
    },
    "dialect": {
        "title": "Database Dialect",
        "description": (
            "The type of database being connected to. Supported values include "
            "mysql, mariadb, mssql, postgresql, oracle, and sqlite."
        ),
        "example": "postgresql",
    },
    "default": {
        "title": "Is Default",
        "description": "If set to True, marks this database configuration as "
        "the default database in a multi-database configuration.",
    },
    "url": {
        "title": "Database URL",
        "description": (
            "A connection string or DSN name. For ODBC, this refers to the DSN name."
        ),
        "example": "postgresql://user:password@localhost/dbname",
    },
    "result_to_dict": {
        "title": "Return results as dict",
        "description": "Return query results as a list of dictionaries.",
    },
    "meta": {
        "title": "meta",
        "description": "This is not used by elixir-db.",
    },
}
