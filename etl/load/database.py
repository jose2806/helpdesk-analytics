import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_SERVER = os.getenv("DATABASE_SERVER")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_DRIVER = os.getenv("DATABASE_DRIVER")
DATABASE_TRUSTED_CONNECTION = os.getenv("DATABASE_TRUSTED_CONNECTION")


def get_connection_string():
    connetion_string = (
        f"DRIVER={{{DATABASE_DRIVER}}};"
        f"SERVER={DATABASE_SERVER};"
        f"DATABASE={DATABASE_NAME};"
        f"Trusted_Connection={DATABASE_TRUSTED_CONNECTION};"
        f"TrustServerCertificate=yes;"
    )
    return "mssql+pyodbc:///?odbc_connect=" + quote_plus(connetion_string)


def get_engine():
    connection_string = get_connection_string()
    return create_engine(connection_string, fast_executemany=True)


def test_connection():
    engine = get_engine()
    with engine.connect() as connection:
        result = connection.execute(text(""" SELECT @@SERVERNAME AS server_name,
            DB_NAME() AS database_name,
            @@VERSION AS sql_version """))
        row = result.fetchone()

        print("================================")
        print(" SQL SERVER CONNECTION TEST")
        print("================================")

        print(f"✓ Server: {row.server_name}")
        print(f"✓ Database: {row.database_name}")
        print("✓ Connection successful")

        print("\nSQL Server version:")
        print(row.sql_version)
