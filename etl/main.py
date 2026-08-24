from etl.config.settings import RAW_DATA_DIR
from etl.extract.csv_reader import load_csv
from etl.quality.validator import (
    validate_tickets,
    validate_relationships,
    validate_transformed_tickets,
)
from etl.transform.cleaner import clean_tickets
from etl.transform.transformer import add_ticket_metrics


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
