"""
Functions for reading SQL queries from the azure SQL warehouse.

All functions will authenticate using Azure Default Credentials. If you are
are working locally the easiest way to set this up is to raise a ticket for
Azure CLI to be installed and set up on your machine. For more complex cases
like authenticating on a remote application, see Azure's own
[docs](https://learn.microsoft.com/en-us/dotnet/api/azure.identity.defaultazurecredential)
"""

import struct
import warnings
import pyodbc

import pandas as pd

from azure.identity import DefaultAzureCredential


def _azure_connection(
    server: str, database: str
) -> pyodbc.Connection:  # pragma: no cover
    """
    Build an azure connection with Default Credential authentication
    """
    possible_drivers: list = [i for i in pyodbc.drivers() if "SQL Server" in i]
    assert len(possible_drivers) > 0, "No available MSSQL drivers"
    driver: str = possible_drivers[0]
    connection_string: str = (
        f"Driver={{{driver}}};Server=tcp:{server},1433;Database={database};"
        "Encrypt=yes;TrustServerCertificate=No;Connection Timeout=30"
    )
    credential = DefaultAzureCredential()
    token_bytes = credential.get_token(
        "https://database.windows.net/.default"
    ).token.encode("UTF-16-LE")
    token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)
    connection = pyodbc.connect(connection_string, attrs_before={1256: token_struct})
    return connection


def query(
    sql: str,
    server: str,
    database: str,
    **kwargs,
) -> pd.DataFrame:
    """
    Run and return the results of a database query for the Azure SQL Warehouse.

    Additional keyword arguments will be passed down to pandas' `read_sql`.

    Note, unless other keyword arguments are passed down, a pyarrow dtype_backend will
    be used by default.
    """
    kwargs = kwargs or {"dtype_backend": "pyarrow"}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return pd.read_sql(
            sql,
            con=_azure_connection(server, database),
            **kwargs,
        )
