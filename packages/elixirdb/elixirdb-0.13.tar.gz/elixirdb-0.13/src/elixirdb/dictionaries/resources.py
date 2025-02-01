"Other resource dictionaries"

from elixirdb.enums import Dialect


drivers = {
    "postgresql": "postgresql+psycopg2",
    "mysql": "mysql+pymysql",
    "sqlite": "sqlite",
    "oracle": "oracle+oracledb",
    "mssql": "mssql+pymssql",
    "mariadb": "mariadb+pymysql",
}

url_keys = (
    "drivername",
    "username",
    "password",
    "host",
    "port",
    "database",
    "query",
)

driver_map = {
    Dialect.MYSQL: "mysql+pymysql",
    Dialect.MARIADB: "mariadb+pymysql",
    Dialect.MSSQL: "mssql+pymssql",
    Dialect.POSTGRESQL: "postgresql+psycopg2",
    Dialect.ORACLE: "oracle+oracledb",
    Dialect.SQLITE: "sqlite",
}
