from etl.config.settings import RAW_DATA_DIR
from etl.extract.csv_reader import load_csv
from etl.quality.validator import validate_tickets, validate_relationships


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


if __name__ == "__main__":
    main()
