USE HelpDesk;
GO

CREATE OR ALTER VIEW dbo.vw_ticket_analytics AS
SELECT
    t.ticket_id,
    t.ticket_number,
    t.created_at,
    t.resolved_at,
    u.user_name,
    d.department_name,
    a.agent_name,
    a.team,
    c.category,
    c.subcategory,
    l.location_name,
    ast.asset_type,
    ast.model,
    t.priority,
    t.status,
    t.channel,
    t.impact,
    t.sla_target_hours,
    t.resolution_hours,
    CASE
        WHEN t.status IN ('Cerrado','Resuelto') AND t.sla_breached = 0 THEN 'Cumplido'
        WHEN t.status IN ('Cerrado','Resuelto') AND t.sla_breached = 1 THEN 'Incumplido'
        ELSE 'Pendiente'
    END AS sla_status,
    t.satisfaction_score,
    CAST(t.created_at AS DATE) AS created_date,
    YEAR(t.created_at) AS created_year,
    MONTH(t.created_at) AS created_month,
    DATENAME(MONTH,t.created_at) AS created_month_name,
    DATENAME(WEEKDAY,t.created_at) AS created_weekday,
    DATEPART(HOUR,t.created_at) AS created_hour
FROM dbo.tickets t
JOIN dbo.users u ON t.user_id=u.user_id
LEFT JOIN dbo.departments d ON u.department_id=d.department_id
LEFT JOIN dbo.agents a ON t.agent_id=a.agent_id
LEFT JOIN dbo.categories c ON t.category_id=c.category_id
LEFT JOIN dbo.locations l ON t.location_id=l.location_id
LEFT JOIN dbo.assets ast ON t.asset_id=ast.asset_id;
GO

CREATE OR ALTER VIEW dbo.vw_helpdesk_kpis AS
SELECT
    COUNT(*) AS total_tickets,
    SUM(CASE WHEN status IN ('Abierto','En progreso') THEN 1 ELSE 0 END) AS open_tickets,
    SUM(CASE WHEN status IN ('Cerrado','Resuelto') THEN 1 ELSE 0 END) AS resolved_tickets,
    CAST(
        100.0 * SUM(CASE WHEN status IN ('Cerrado','Resuelto') AND sla_breached=0 THEN 1 ELSE 0 END)
        / NULLIF(SUM(CASE WHEN status IN ('Cerrado','Resuelto') THEN 1 ELSE 0 END),0)
        AS DECIMAL(10,2)
    ) AS sla_compliance_pct,
    CAST(AVG(resolution_hours) AS DECIMAL(10,2)) AS avg_resolution_hours,
    CAST(AVG(CAST(satisfaction_score AS DECIMAL(10,2))) AS DECIMAL(10,2)) AS avg_satisfaction
FROM dbo.tickets;
GO
