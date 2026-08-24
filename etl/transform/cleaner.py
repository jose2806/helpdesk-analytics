import pandas as pd


def clean_tickets(tickets: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and normalize the tickets data set.
    """

    df = tickets.copy()

    # Remove duplicated rows
    df = df.drop_duplicates()

    # Normalize text fields
    text_column = ["ticket_number", "priority", "status"]

    for column in text_column:
        if column in df.columns:
            df[column] = df[column].astype("string").str.strip()

    # Convert dates
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    if "resolved_at" in df.columns:
        df["resolved_at"] = pd.to_datetime(df["resolved_at"], errors="coerce")

    return df
