import pandas as pd
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


def main():

    print("================================")
    print("       HELPDESK ETL")
    print("================================")

    print("\n[1/5] Extracting data...")

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

    print("\n[2/5] Validating data...")

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

    print("\n[LOAD TEST] Loading users into SQL Server...")

    engine = get_engine()
    ##users.to_sql("users", schema="stg", con=engine, if_exists="appennd", index=False)
    users.to_sql("users", schema="stg", con=engine, if_exists="replace", index=False)
    ##agents.to_sql("agents", schema="stg", con=engine, if_exists="apend", index=False)
    agents.to_sql("agents", schema="stg", con=engine, if_exists="replace", index=False)
    """ categories.to_sql(
        "categories", schema="stg", con=engine, if_exists="append", index=False
    ) """
    categories.to_sql(
        "categories", schema="stg", con=engine, if_exists="replace", index=False
    )
    """ departments.to_sql(
        "departments", schema="stg", con=engine, if_exists="append", index=False
    ) """
    departments.to_sql(
        "departments", schema="stg", con=engine, if_exists="replace", index=False
    )
    """ locations.to_sql("locations", schema="stg", con=engine, if_exists="append",index=False) """
    locations.to_sql(
        "locations", schema="stg", con=engine, if_exists="replace", index=False
    )
    """ assets.to_sql("assets",schema="stg",con=engine,if_exists="append", index=False) """
    assets.to_sql("assets", schema="stg", con=engine, if_exists="replace", index=False)

    print(f"✓ Users loaded into stg.users: " f"{len(users):,}")
    print(f"✓ Agents loaded into stg.agents: " f"{len(agents):,}")
    print(f"✓ Categories loaded into stg.categories: " f"{len(categories):,}")
    print(f"✓ Departments loaded into stg.departments: " f"{len(departments):,}")
    print(f"✓ Locations loaded into stg.locations: " f"{len(locations):,}")
    print(f"✓ Assets loaded into stg.assets: " f"{len(assets):,}")

    print("\n[DATE DIMENSION] Generating date dimension...")
    tickets["created_at"] = pd.to_datetime(tickets["created_at"])
    start_date = tickets["created_at"].min().date()
    end_date = tickets["created_at"].max().date()

    date_dimension = generate_date_dimension(start_date, end_date)
    loaded_dates = load_date_dimension(date_dimension, engine)
    print(f"✓ Dates loaded into dw.dim_date: " f"{loaded_dates:,}")

    # ==============================
    # CLEAN
    # ==============================

    print("\n[3/5] Cleaning data...")

    tickets = clean_tickets(tickets)

    print(f"✓ Tickets after cleaning: " f"{len(tickets):,}")

    # ==============================
    # TRANSFORM
    # ==============================

    print("\n[4/5] Transforming data...")

    tickets = add_ticket_metrics(tickets)

    print("✓ Ticket metrics generated")

    # ==============================
    # TRANSFORMED DATA QUALITY
    # ==============================

    print("\n[5/5] Validating transformed data...")

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
