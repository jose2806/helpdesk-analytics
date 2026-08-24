import pandas as pd


def validate_required_columns(
    df: pd.DataFrame, required_columns: list[str]
) -> list[str]:

    errors = []

    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    if missing_columns:
        errors.append(f"Missing columns: {missing_columns}")

    return errors


def validate_unique(df: pd.DataFrame, column: str) -> list[str]:
    errors = []
    duplicates = df[column].duplicated().sum()
    if duplicates > 0:
        errors.append(f"{column}: {duplicates} duplicates values")
    return errors


def validate_allowed_values(
    df: pd.DataFrame, column: str, allowed_values: set
) -> list[str]:
    errors = []
    invalid_values = set(df[column].dropna().unique()) - allowed_values

    """ realiza la resta o diferencia de conjuntos.
    Toma los valores presentes en el DataFrame y les quita los permitidos.
    Lo que sobra son los valores no autorizados. """

    if invalid_values:
        errors.append(f"{column}: invalid values" f"{invalid_values}")
    return errors


def validate_numeric_range(
    df: pd.DataFrame, column: str, minimum: float, maximum: float | None = None
) -> list[str]:

    errors = []
    values = df[column].dropna()
    invalid = values < minimum
    if maximum is not None:
        invalid |= values > maximum
    invalid_count = invalid.sum()
    if invalid_count > 0:
        errors.append(f"{column}: {invalid_count}" f"values outside valid range")
    return errors


def validate_tickets(tickets: pd.DataFrame) -> list[str]:

    errors = []
    required_columns = [
        "ticket_id",
        "ticket_number",
        "created_at",
        "user_id",
        "agent_id",
        "category_id",
        "priority",
        "status",
        "sla_breached",
    ]

    errors.extend(validate_required_columns(tickets, required_columns))

    if "ticket_id" in tickets.columns:
        errors.extend(validate_unique(tickets, "ticket_id"))

    if "ticket_number" in tickets.columns:
        errors.extend(validate_unique(tickets, "ticket_number"))

    if "priority" in tickets.columns:
        errors.extend(
            validate_allowed_values(
                tickets, "priority", {"Baja", "Media", "Alta", "Crítica"}
            )
        )

    if "satisfaction_score" in tickets.columns:
        errors.extend(validate_numeric_range(tickets, "satisfaction_score", 1, 5))

    if "resolution_hours" in tickets.columns:
        errors.extend(validate_numeric_range(tickets, "resolution_hours", 0))

    if "sla_breached" in tickets.columns:
        errors.extend(validate_allowed_values(tickets, "sla_breached", {0, 1}))

    return errors


def validate_foreign_key(child_df, child_column, parent_df, parent_column):
    errors = []

    child_values = set(child_df[child_column].dropna().unique())

    parent_values = set(parent_df[parent_column].dropna().unique())

    invalid = child_values - parent_values

    if invalid:
        errors.append(f"{child_column}: {len(invalid)}")

    return errors


def validate_relationships(tickets, users, agents, categories, assets):
    errors = []

    errors.extend(validate_foreign_key(tickets, "user_id", users, "user_id"))

    errors.extend(validate_foreign_key(tickets, "agent_id", agents, "agent_id"))

    errors.extend(
        validate_foreign_key(tickets, "category_id", categories, "category_id")
    )

    errors.extend(validate_foreign_key(tickets, "asset_id", assets, "asset_id"))

    return errors
