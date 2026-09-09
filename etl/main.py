import pandas as pd
from sqlalchemy import text
from etl.config.settings import RAW_DATA_DIR
from etl.extract.csv_reader import load_csv
from etl.quality.validator import (
    validate_tickets,
    validate_relationships,
    validate_transformed_tickets,
)
from etl.transform.cleaner import clean_tickets
from etl.transform.transformer import add_ticket_metrics
from etl.load.database import get_engine
from etl.transform.date_dimension import generate_date_dimension, load_date_dimension
from etl.load.staging import load_staging


def main():

    print("================================")
    print("       HELPDESK ETL")
    print("================================")

    # ==============================
    # EXTRACTION
    # ==============================
    print("\n[1/6] Extracting data...")

    tickets = load_csv("tickets.csv", RAW_DATA_DIR)
    users = load_csv("users.csv", RAW_DATA_DIR)
    agents = load_csv("agents.csv", RAW_DATA_DIR)
    categories = load_csv("categories.csv", RAW_DATA_DIR)
    departments = load_csv("departments.csv", RAW_DATA_DIR)
    locations = load_csv("locations.csv", RAW_DATA_DIR)
    assets = load_csv("assets.csv", RAW_DATA_DIR)
    ticket_events = load_csv("ticket_events.csv", RAW_DATA_DIR)

    print(f"Tickets: {len(tickets):,}")
    print(f"Users: {len(users):,}")
    print(f"Agents: {len(agents):,}")
    print(f"Categories: {len(categories):,}")
    print(f"Departments: {len(departments):,}")
    print(f"Locations: {len(locations):,}")
    print(f"Assets: {len(assets):,}")
    print(f"Ticket events: {len(ticket_events):,}")

    print("\n[2/6] Validating data...")

    # ==============================
    # VALIDATION
    # ==============================

    errors = validate_tickets(tickets)

    if errors:
        print("\n❌ DATA QUALITY ERRORS")
        for error in errors:
            print(f" - {error}")

        raise SystemExit("ETL stopped due to data quality errors.")
    print("✓ Ticket validation passed")

    relationship_errors = validate_relationships(
        tickets, users, agents, categories, assets
    )

    if relationship_errors:
        print("\n❌ RELATIONSHIP ERRORS")

        for error in relationship_errors:
            print(f" - {error}")
        raise SystemExit("ETL stopped due to relationship errors.")
    print("✓ Relationship validation passed")

    # ==============================
    # CLEAN
    # ==============================

    print("\n[3/6] Cleaning data...")

    tickets = clean_tickets(tickets)

    print(f"✓ Tickets after cleaning: " f"{len(tickets):,}")

    # ==============================
    # TRANSFORM
    # ==============================

    print("\n[4/6] Transforming data...")

    tickets = add_ticket_metrics(tickets)

    print("✓ Ticket metrics generated")

    # ==============================
    # LOAD
    # ==============================

    print("\n[5/6] Loading data into SQL Server...")

    engine = get_engine()

    load_staging(
        engine=engine,
        tickets=tickets,
        users=users,
        agents=agents,
        categories=categories,
        departments=departments,
        locations=locations,
        assets=assets,
    )
    print("\n[DATE DIMENSION] Generating date dimension...")
    tickets["created_at"] = pd.to_datetime(tickets["created_at"])
    start_date = tickets["created_at"].min().date()
    end_date = tickets["created_at"].max().date()

    date_dimension = generate_date_dimension(start_date, end_date)
    loaded_dates = load_date_dimension(date_dimension, engine)
    print(f"✓ Dates loaded into dw.dim_date: " f"{loaded_dates:,}")

    # ==============================
    # LOAD FACT TABLE
    # ==============================

    print("\n[FACT TABLE] Loading dw.fact_tickets...")

    with engine.begin() as connection:
        connection.execute(text("EXEC dw.sp_load_fact_tickets"))
    print("✓ Fact table loaded successfully")

    # ==============================
    # FACT TABLE VALIDATION
    # ==============================

    with engine.connect() as connection:
        staging_count = connection.execute(
            text("SELECT COUNT(*) FROM stg.tickets")
        ).scalar_one()
        fact_count = connection.execute(
            text("SELECT COUNT(*) FROM dw.fact_tickets")
        ).scalar_one()
        null_asset_count = connection.execute(
            text("SELECT COUNT(*) FROM dw.fact_tickets WHERE asset_key is NULL")
        ).scalar_one()
        unknown_asset_count = connection.execute(
            text("SELECT COUNT(*) FROM dw.fact_tickets WHERE asset_key = 0")
        ).scalar_one()

    print(f"✓ Staging tickets: {staging_count:,}")
    print(f"✓ Fact tickets: {fact_count:,}")
    print(f"✓ Tickets with NULL asset_key: {null_asset_count:,}")
    print(f"✓ Tickets using Unknown Asset: {unknown_asset_count:,}")

    if staging_count != fact_count:
        raise SystemExit("ETL stopped: staging and fact ticket counts do not match.")
    if null_asset_count != 0:
        raise SystemExit("ETL stopped: fact_tickets contains NULL asset_key values.")
    print("✓ Fact table validation passed")

    # ==============================
    # TRANSFORMED DATA QUALITY
    # ==============================

    print("\n[6/6] Validating transformed data...")

    transformed_errors = validate_transformed_tickets(tickets)

    if transformed_errors:
        print("\n❌ TRANSFORMATION ERRORS")

        for error in transformed_errors:
            print(f" - {error}")

        raise SystemExit("ETL stopped after transformation.")

    print("✓ Transformed data validation passed")

    print("\n========== TRANSFORMATION SUMMARY ==========")

    print(f"Total tickets: {len(tickets):,}")

    print(f"Backlog tickets: " f"{tickets['backlog_flag'].sum():,}")

    print(f"High/Critical tickets: " f"{tickets['high_priority_flag'].sum():,}")

    print(f"Resolved tickets: " f"{tickets['resolution_hours'].notna().sum():,}")

    print(f"Average SLA utilization: " f"{tickets['sla_utilization'].mean():.2%}")


if __name__ == "__main__":
    main()
