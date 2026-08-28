import pandas as pd


def generate_date_dimension(start_date, end_date):
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    df = pd.DataFrame(
        {
            "date_key": dates.strftime("%Y%m%d").astype(int),
            "full_date": dates,
            "year_number": dates.year,
            "quarter_number": dates.quarter,
            "month_number": dates.month,
            "month_name": dates.strftime("%B"),
            "week_number": dates.isocalendar().week.astype(int),
            "day_number": dates.day,
            "day_name": dates.day_name(),
            "is_weekend": dates.dayofweek >= 5,
        }
    )

    return df


def load_date_dimension(date_dimension, engine):
    existing_dates = pd.read_sql("SELECT date_key FROM dw.dim_date", engine)
    if not existing_dates.empty:
        date_dimension = date_dimension[
            ~date_dimension["date_key"].isin(existing_dates["date_key"])
        ]

    if date_dimension.empty:
        print("✓ Date dimension already up to date")
        return 0

    date_dimension.to_sql(
        "dim_date", schema="dw", con=engine, if_exists="append", index=False
    )

    return len(date_dimension)
