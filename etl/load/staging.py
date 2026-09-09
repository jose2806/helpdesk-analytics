import pandas as pd
from sqlalchemy import text


def clear_staging(engine):
    """Limpiar las tablas de staging antes de una nueva carga"""
    tables = [
        "users",
        "tickets",
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


def load_staging(
    engine, tickets, users, agents, categories, departments, locations, assets
):
    """Carga los DataFrames en las tablas de staging"""

    clear_staging(engine)

    # =====================================================
    # TICKETS
    # Solo columnas existentes en stg.tickets
    # =====================================================

    ticket_columns = [
        "ticket_id",
        "ticket_number",
        "user_id",
        "agent_id",
        "category_id",
        "location_id",
        "asset_id",
        "priority",
        "status",
        "created_at",
        "resolved_at",
        "resolution_hours",
        "satisfaction_score",
        "sla_target_hours",
        "sla_breached",
        "sla_compliant",
        "sla_utilization",
        "backlog_flag",
        "high_priority_flag",
        "resolution_bucket",
        "is_weekend",
    ]
    tickets_staging = tickets[ticket_columns].copy()

    # =====================================================
    # DERIVAR DEPARTMENT_ID DESDE EL USUARIO
    # =====================================================

    user_departments = users[["user_id", "department_id"]].copy()

    tickets_staging = tickets_staging.merge(
        user_departments,
        on="user_id",
        how="left",
    )
    missing_departments = tickets_staging["department_id"].isna().sum()

    if missing_departments > 0:
        print(f"⚠ Tickets sin departamento: " f"{missing_departments:,}")
    else:
        print("✓ Department IDs assigned to all tickets")

    # =====================================================
    # ORDENAR COLUMNAS SEGÚN stg.tickets
    # =====================================================

    ticket_columns_final = [
        "ticket_id",
        "ticket_number",
        "user_id",
        "agent_id",
        "category_id",
        "department_id",
        "location_id",
        "asset_id",
        "priority",
        "status",
        "created_at",
        "resolved_at",
        "resolution_hours",
        "satisfaction_score",
        "sla_target_hours",
        "sla_breached",
        "sla_compliant",
        "sla_utilization",
        "backlog_flag",
        "high_priority_flag",
        "resolution_bucket",
        "is_weekend",
    ]

    tickets_staging = tickets_staging[ticket_columns_final]

    # =====================================================
    # DATASETS
    # =====================================================
    datasets = {
        "users": users,
        "tickets": tickets_staging,
        "agents": agents,
        "categories": categories,
        "departments": departments,
        "locations": locations,
        "assets": assets,
    }

    # =====================================================
    # LOAD
    # =====================================================
    for table_name, dataframe in datasets.items():
        dataframe.to_sql(
            table_name, schema="stg", con=engine, if_exists="append", index=False
        )

        print(f"✓ {table_name}: " f"{len(dataframe):,} rows loaded")
