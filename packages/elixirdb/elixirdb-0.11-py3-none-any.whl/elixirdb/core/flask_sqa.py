# """Wrapper class to check for flask"""


# def requires_flasksqlalchemy(func):
#     "Ensure that Flask is installed before running the decorated function."

#     def wrapper(*args, **kwargs):
#         try:
#             from flask_sqlalchemy import SQLAlchemy
#         except ImportError:
#             raise ImportError(
#                 "Flask is not installed. Install it to use Flask functionality."
#             ) from None
#         return func(*args, **kwargs)

#     return wrapper


#         @requires_flasksqlalchemy
#         class FlaskSqlalchemyConnection(ElixirDB, SQLAlchemy):
#             """
#             A combined class for use with FlaskSqlAlchemy.

#             Using this class means you will not be able to

#             """

#             def __call__(self, *args: Any, **kwds: Any) -> Any:
#                 config = kwargs.pop(config)
#                 name = kwargs.pop(name)
#                 enable_statements = kwargs.pop(enable_statements)
#                 engine_type = kwargs.pop(engine_type)

#                 SQLAlchemy.__init__()
