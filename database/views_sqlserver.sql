USE HelpDeskAnalytics;
GO

/* ============================================================
   VISTA 1 — KPIs EJECUTIVOS
   ============================================================ */

CREATE OR ALTER VIEW dw.vw_executive_kpis
AS
SELECT
    COUNT(*) AS total_tickets,
    SUM(CASE WHEN backlog_flag = 1 THEN 1 ELSE 0 END) 
	AS backlog_tickets,
    SUM(CASE WHEN high_priority_flag = 1 THEN 1 ELSE 0 END)
	AS high_critical_tickets,
    SUM(CASE WHEN resolved_at IS NOT NULL THEN 1 ELSE 0 END) 
	AS resolved_tickets,
    CAST(100.0 * SUM(CASE WHEN resolved_at IS NOT NULL AND 
	sla_compliant = 1 THEN 1 ELSE 0 END)
    / NULLIF(SUM(CASE WHEN resolved_at IS NOT NULL THEN 1 ELSE 0 END), 
	0) AS DECIMAL(10,2)) AS sla_compliance_pct,
	CAST(AVG(CASE WHEN resolved_at IS NOT NULL THEN resolution_hours END) 
	AS DECIMAL(10,2)) AS avg_resolution_hours,
    CAST(AVG(CASE WHEN satisfaction_score IS NOT NULL THEN satisfaction_score END)
	AS DECIMAL(10,2)) AS avg_satisfaction,
	SUM(CASE WHEN resolved_at IS NOT NULL THEN 1 ELSE 0 END) 
	AS resolved_ticket_count
FROM dw.fact_tickets;
GO

/* ============================================================
   VISTA 2 — TENDENCIA MENSUAL
   ============================================================ */

CREATE OR ALTER VIEW dw.vw_mothly_trend
AS 
SELECT d.year_number,d.month_number,d.month_name, COUNT(*) AS total_tickets,
SUM(CASE WHEN f.backlog_flag = 1 THEN 1 ELSE 0 END) AS backlog_tickets,
SUM(CASE WHEN f.sla_breached = 1 THEN 1 ELSE 0 END) AS sla_breaches,
CAST(AVG(f.resolution_hours) AS DECIMAL(10,2)) AS avg_resolution_hours,
CAST(AVG(f.satisfaction_score) AS DECIMAL(10,2)) AS avg_satisfaction
FROM dw.fact_tickets f INNER JOIN dw.dim_date d ON f.date_key = d.date_key
GROUP BY d.year_number, d.month_number, d.month_name;
GO

/* ============================================================
   VISTA 3 — DESEMPEÑO POR AGENTE
   ============================================================ */

 CREATE OR ALTER VIEW dw.vw_agent_performance
 AS
 SELECT a.agent_key, a.agent_id, a.agent_name, a.team, a.seniority,
 COUNT(*) AS total_tickets,
 SUM(CASE WHEN f.resolved_at IS NOT NULL THEN 1 ELSE 0 END) AS resolved_tickets,
 SUM(CASE WHEN f.sla_breached = 1 THEN 1 ELSE 0 END) AS sla_breaches,
 CAST(100.0 * SUM(CASE WHEN f.sla_breached = 0 THEN 1 ELSE 0 END)
 / NULLIF(COUNT(*),0) AS DECIMAL(5,2)) AS sla_compliance_pct,
 CAST(AVG(f.resolution_hours) AS DECIMAL(10,2)) AS avg_resolution_hours,
 CAST(AVG(f.satisfaction_score) AS DECIMAL(10,2)) AS avg_satisfaction
 FROM dw.fact_tickets f INNER JOIN dw.dim_agents a ON f.agent_key = a.agent_key
 GROUP BY a.agent_key, a.agent_id, a.agent_name, a.team, a.seniority;
 GO

 /* ============================================================
   VISTA 4 — DESEMPEÑO POR CATEGORÍA
   ============================================================ */

CREATE OR ALTER VIEW dw.vw_category_performance
AS
SELECT c.category_key,c.category_id,c.category_name,
c.subcategory_name,COUNT(*) AS total_tickets,
SUM(CASE WHEN f.sla_breached = 1 THEN 1 ELSE 0 END) AS sla_breaches,
CAST(100.0 * SUM(CASE WHEN f.sla_breached = 0 THEN 1 ELSE 0 END)
/ NULLIF(COUNT(*),0) AS DECIMAL(5,2)) AS sla_compliance_pct,
CAST(AVG(f.resolution_hours) AS DECIMAL(10,2)) AS avg_resolution_hours,
CAST(AVG(f.satisfaction_score) AS decimal(10,2)) AS avg_satisfaction
FROM dw.fact_tickets f INNER JOIN dw.dim_categories c ON f.category_key = c.category_key
GROUP BY c.category_key,c.category_id,c.category_name,c.subcategory_name;
GO

/* ============================================================
   VISTA 5 — PRIORIDAD / SLA
   ============================================================ */

CREATE OR ALTER VIEW dw.vw_priority_performance
AS 
SELECT priority, COUNT(*) AS total_tickets,
SUM(CASE WHEN sla_breached = 1 THEN 1 ELSE 0 END) AS sla_breaches,
CAST(100.0 * SUM(CASE WHEN sla_breached = 0 THEN 1 ELSE 0 END)
/ NULLIF(COUNT(*),0) AS DECIMAL(5,2)) AS sla_compliance_pct,
CAST(AVG(resolution_hours) AS DECIMAL(10,2)) AS avg_resolution_hours,
CAST(AVG(satisfaction_score) AS DECIMAL(10,2)) AS avg_satisfactionn
FROM dw.fact_tickets
GROUP BY priority;
GO

/* ============================================================
   VISTA 6 — DEPARTAMENTO
   ============================================================ */

CREATE OR ALTER VIEW dw.vw_department_performance
AS
SELECT d.department_key, d.department_id, d.department_name,
COUNT(*) AS total_tickets,
SUM(CASE WHEN f.backlog_flag = 1 THEN 1 ELSE 0 END) AS backlog_tickets,
SUM(CASE WHEN f.sla_breached = 1 THEN 1 ELSE 0 END)AS sla_breaches,
CAST(100.0 * SUM(CASE WHEN f.sla_breached = 0 THEN 1 ELSE 0 END)
/ NULLIF(COUNT(*),0) AS DECIMAL(5,2)) AS sla_compliance_pct,
CAST(AVG(f.resolution_hours) AS DECIMAL(10,2)) AS avg_resolution_hours,
CAST(AVG(f.satisfaction_score) AS DECIMAL(10,2)) AS avg_satisfaction
FROM dw.fact_tickets f INNER JOIN dw.dim_departments d ON f.department_key = d.department_key
GROUP BY d.department_key, d.department_id, d.department_name;
GO