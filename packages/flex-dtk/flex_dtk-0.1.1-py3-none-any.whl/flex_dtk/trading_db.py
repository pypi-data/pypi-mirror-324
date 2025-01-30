"""
Functions for reading SQL queries from the trading db.

Note that Azure authentication is not possible on the postgres-db, you will need
to securely store username and password data using a package such as "keyring".
"""

import pandas as pd
from sqlalchemy import create_engine


def _postgres_engine(server: str, database: str, username: str, password: str):
    """
    Return engine for postgres based on given settings
    """
    return create_engine(
        f"postgresql://{username}:{password}@{server}:5432/{database}",
    )


def query(
    sql: str,
    server: str,
    database: str,
    username: str,
    password: str,
    **kwargs,
) -> pd.DataFrame:
    """
    Run and return the results of a database query for the Postgres trading database
    """
    kwargs = kwargs or {"dtype_backend": "pyarrow"}
    return pd.read_sql(
        sql,
        con=_postgres_engine(server, database, username, password),
        **kwargs,
    )
