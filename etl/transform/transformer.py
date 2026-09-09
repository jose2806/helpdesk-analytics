import pandas as pd


def add_ticket_metrics(tickets: pd.DataFrame) -> pd.DataFrame:

    df = tickets.copy()

    # ==========================================
    # DATE DIMENSIONS
    # ==========================================

    df["created_date"] = df["created_at"].dt.date

    df["created_year"] = df["created_at"].dt.year

    df["created_month"] = df["created_at"].dt.month

    df["created_month_name"] = df["created_at"].dt.month_name()

    df["created_day"] = df["created_at"].dt.day

    df["created_day_of_week"] = df["created_at"].dt.day_of_week

    df["created_day_name"] = df["created_at"].dt.day_name()

    df["created_hour"] = df["created_at"].dt.hour

    # ==========================================
    # WEEKEND
    # ==========================================

    df["is_weekend"] = (df["created_day_of_week"]) >= 5

    # ==========================================
    # BACKLOG
    # ==========================================

    df["backlog_flag"] = df["status"].isin(["Abierto", "En progreso"])

    # ==========================================
    # HIGH PRIORITY
    # ==========================================

    df["high_priority_flag"] = df["priority"].isin(["Alta", "Crítica"])

    # ==========================================
    # SLA UTILIZATION
    # ==========================================
    # SLA is evaluated only for tickets that have been resolved.
    # A resolved ticket breaches SLA when resolution_hours exceeds
    # the configured SLA target. Unresolved tickets are not treated
    # as compliant or breached yet.

    resolved_mask = df["resolution_hours"].notna()
    valid_sla_mask = (
        resolved_mask & df["sla_target_hours"].notna() & (df["sla_target_hours"] > 0)
    )
    df["sla_breached"] = False
    df.loc[valid_sla_mask, "sla_breached"] = (
        df.loc[valid_sla_mask, "resolution_hours"]
        > df.loc[valid_sla_mask, "sla_target_hours"]
    )

    df["sla_compliant"] = False
    df.loc[valid_sla_mask, "sla_compliant"] = (
        df.loc[valid_sla_mask, "resolution_hours"]
        <= df.loc[valid_sla_mask, "sla_target_hours"]
    )

    # SLA utilization is only meaningful for resolved tickets.
    df["sla_utilization"] = pd.NA
    df.loc[valid_sla_mask, "sla_utilization"] = (
        df.loc[valid_sla_mask, "resolution_hours"]
        / df.loc[valid_sla_mask, "sla_target_hours"]
    )

    # ==========================================
    # RESOLUTION BUCKET
    # ==========================================

    df["resolution_bucket"] = pd.cut(
        df["resolution_hours"],
        bins=[-float("inf"), 4, 8, 24, 48, float("inf")],
        labels=["< 4h", "4-8h", "8-24h", "24-48h", "> 48h"],
    )

    return df
