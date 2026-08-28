import pandas as pd
from sqlalchemy import text


def clear_staging(engine):
    """Limpiar las tablas de staging antes de una nueva carga"""
    tables = [
        "users",
        "agents",
        "categories",
        "departments",
        "locations",
        "assets",
    ]
    with engine.begin() as connection:
        for table in tables:
            connection.execute(text(f"TRUNCATE TABLE stg.{table}"))
    print("✓ Staging tables cleared")


def load_staging(engine, users, agents, categories, departments, locations, assets):
    """Carga los DataFrames en las tablas de staging"""

    clear_staging(engine)
    datasets = {
        "users": users,
        "agents": agents,
        "categories": categories,
        "departments": departments,
        "locations": locations,
        "assets": assets,
    }
    for table_name, dataframe in datasets.items():
        dataframe.to_sql(
            table_name, schema="stg", con=engine, if_exists="append", index=False
        )

        print(f"✓ {table_name}: " f"{len(dataframe):,} rows loaded")
