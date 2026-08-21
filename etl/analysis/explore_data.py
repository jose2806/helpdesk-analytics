import pandas as pd
from pathlib import Path

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.max_rows", 100)

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "raw"

tickets = pd.read_csv(DATA_DIR / "tickets.csv")
categories = pd.read_csv(DATA_DIR / "categories.csv")
agents = pd.read_csv(DATA_DIR / "agents.csv")
users = pd.read_csv(DATA_DIR / "users.csv")
departments= pd.read_csv(DATA_DIR / "departments.csv")

print("Dataset cargado correctammente")
print(f"Filas: {len(tickets):,}")
print(f"Columnas: {len(tickets.columns)}")

print("\nColumnas:")
print(tickets.columns.tolist())

print("\nPrimeras filas:")
print(tickets.head())

print("\nÚltimas filas:")
print(tickets.tail())

print("\nInformación:")
tickets.info()

print("\nTipos de datos:")
print(tickets.dtypes)

""" print("\nValores nulos:")
nulls = tickets.isnull().sum()

print(nulls[nulls > 0]) """

null_report = pd.DataFrame({
  "null_count": tickets.isnull().sum(),
  "null_percentage": tickets.isnull().mean() * 100
})

null_report = null_report[
  null_report["null_count"] > 0
].sort_values(
  "null_percentage",
  ascending=False
)

print("\nReporte de valores nulos:")
print(null_report)

print("\nTickets duplicados:")
print(tickets.duplicated().sum())

duplicates = tickets[
  tickets["ticket_number"].duplicated(keep=False)
]

print("\nTicket numbers duplicados:")
print(duplicates[["ticket_id", "ticket_number"]])

print("\nTickets por prioridad:")
print(
  tickets["priority"].value_counts()
)

print("\nPorcentaje por prioridad:")
print(
  tickets["priority"].value_counts(normalize=True).mul(100).round(2)
)

print("\nTickets por estado:")
print(tickets["status"].value_counts())

open_statuses = ["Abierto", "En progreso"]
open_tickets = tickets[
  tickets["status"].isin(open_statuses)
]

print(f"\nTickets abiertos / en progreso: {len(open_tickets):,}")

print("\nTickets por categoria:")
print(
  tickets["category_id"].value_counts().head(10)
)

print("\nCumplimiento SLA:")
print(tickets["sla_breached"].value_counts())

resolved = tickets[
  tickets["status"].isin(["Cerrado","Reselto"])
]

sla_compliance = (
  resolved["sla_breached"].eq(0).mean() *100
)

print(f"\nCumplimiento SLA: {sla_compliance: .2f}%")

avg_resolution = resolved["resolution_hours"].mean()

print(f"\nTiemmpo promedio de reslucion: " f"{avg_resolution:.2f} horas")

print("\nEstadisticas de resolucion:")
print(
  resolved["resolution_hours"].describe()
)

slow_tickets = resolved[
  resolved["resolution_hours"] > 48
]

print( 
  f"\nTickets con mas de 48 horas: "
  f"{len(slow_tickets)}"
)

print(
  slow_tickets[
    [
      "ticket_number",
      "priority",
      "status",
      "resolution_hours",
      "sla_breached"
    ]
  ].head(20)
)

print("\nSatifaccion:")
print(
  resolved["satisfaction_score"].value_counts().sort_index()
)

avg_satisfaction= resolved["satisfaction_score"].mean()

print(f"\nSatisfacion promedio: {avg_satisfaction:.2f}/5" )

tickets_by_hour = (
  tickets["created_hour"].value_counts().sort_index()
)

print(f"\nTickets por hora:")
print(tickets_by_hour)

print("\nTickets por dia:")
print(
  tickets["created_weekday"].value_counts()
)

print("\n========== DATASET SUMMARY ==========")

print(f"Total tickets: {len(tickets):,}")
print(f"Usuarios únicos: {tickets['user_id'].nunique():,}")
print(f"Agentes únicos: {tickets['agent_id'].nunique():,}")
print(f"Tickets abiertos: {len(open_tickets):,}")
print(f"SLA compliance: {sla_compliance:.2f}%")
print(f"Avg resolution: {avg_resolution:.2f} hours")
print(f"Avg satisfaction: {avg_satisfaction:.2f}/5")

print("\n========== PRIORIDAD ==========")

priority_analysis = (
    tickets
    .groupby("priority")
    .agg(
        tickets=("ticket_id", "count"),
        avg_resolution=("resolution_hours", "mean"),
        sla_breach_rate=("sla_breached", "mean"),
        satisfaction=("satisfaction_score", "mean")
    )
    .sort_values("tickets", ascending=False)
)

priority_analysis["sla_breach_rate"] *= 100

print(priority_analysis.round(2))

ticket_categories = tickets.merge(categories, on="category_id",how="left")

category_analysis = (
  ticket_categories
  .groupby(["category", "subcategory"])
  .agg(
    tickets=("ticket_id", "count"),
    avg_resolution=("resolution_hours", "mean"),
    sla_breach_rate=("sla_breached", "mean"),
    satisfaction=("satisfaction_score", "mean")
  ).sort_values("tickets", ascending=False)
)

category_analysis["sla_breach_rate"]*100

print("\n========== CATEGORÍAS ==========")
print(category_analysis.head(15).round(2))

tickets_agents= tickets.merge(
  agents, on="agent_id",how="left"
)

agent_analysis = (
  tickets_agents
  .groupby(["agent_name","team","seniority"])
  .agg(
    tickets=("ticket_id", "count"),
    avg_resolution=("resolution_hours", "mean"),
    sla_breach_rate=("sla_breached", "mean"),
    satisfaction=("satisfaction_score", "mean")
  ).sort_values("tickets",ascending=False)
)
agent_analysis["sla_breach_rate"] *= 100

print("\n========== AGENTES ==========")
print(agent_analysis.round(2))

sla_satisfaction=(
  tickets[
  tickets["satisfaction_score"].notna()
  ]
  .groupby("sla_breached")
  .agg(
    tickets=("ticket_id", "count"),
    avg_satisfaction=("satisfaction_score", "mean"),
    avg_resolution=("resolution_hours", "mean")
  )
)

print("\n========== SLA VS SATISFACCIÓN ==========")
print(sla_satisfaction.round(2))

backlog = tickets[tickets["status"].isin(["Abierto", "En progreso"])]

backlog_analysis = (
  backlog
  .groupby("priority")
  .agg(
    tickets=("ticket_id", "count")
  ).sort_values("tickets", ascending=False)
)

print("\n========== BACKLOG ==========")
print(backlog_analysis)

full_tickets = tickets.merge(
  users[[
    "user_id",
    "department_id"
  ]],
  on="user_id", how="left"
)

full_tickets= full_tickets.merge(
  departments, on="department_id", how="left"
)

full_tickets= full_tickets.merge(
  categories, on="category_id", how="left"
)

department_analysis = (
  full_tickets
  .groupby("department_name")
  .agg(
    tickets=("ticket_id", "count"),
    avg_resolution=("resolution_hours", "mean"),
    sla_breach_rate=("sla_breached", "mean"),
    satisfaction=("satisfaction_score", "mean")
  ).sort_values("tickets",ascending=False)
)

department_analysis["sla_breach_rate"] *= 100

print("\n========== DEPARTAMENTOS ==========")
print(department_analysis.round(2))

resolved["sla_utilization"] = (
    resolved["resolution_hours"] /
    resolved["sla_target_hours"]
) * 100

print("\n========== SLA UTILIZATION ==========")

print(
    resolved[
        "sla_utilization"
    ].describe().round(2)
)

print("\nPromedio de utilización del SLA:")

print(
    f"{resolved['sla_utilization'].mean():.2f}%"
)