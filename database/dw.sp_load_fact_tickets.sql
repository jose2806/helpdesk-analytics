CREATE OR ALTER PROCEDURE dw.sp_load_fact_tickets
AS
BEGIN
    SET NOCOUNT ON;

    MERGE INTO dw.fact_tickets AS target

    USING
    (
        SELECT
            t.ticket_id,
            t.ticket_number,

            d.date_key,
            u.user_key,
            a.agent_key,
            c.category_key,
            dep.department_key,
            loc.location_key,
            ISNULL(ast.asset_key, 0) AS asset_key,

            t.priority,
            t.status,
            t.created_at,
            t.resolved_at,
            t.resolution_hours,
            t.satisfaction_score,
            t.sla_target_hours,
            t.sla_breached,
            t.sla_compliant,
            t.sla_utilization,
            t.backlog_flag,
            t.high_priority_flag,
            t.resolution_bucket,
            t.is_weekend

        FROM stg.tickets AS t

        LEFT JOIN dw.dim_date AS d
            ON d.date_key =
                CAST(CONVERT(VARCHAR(8), t.created_at, 112) AS INT)

        LEFT JOIN dw.dim_users AS u
            ON t.user_id = u.user_id

        LEFT JOIN dw.dim_agents AS a
            ON t.agent_id = a.agent_id

        LEFT JOIN dw.dim_categories AS c
            ON t.category_id = c.category_id

        LEFT JOIN dw.dim_departments AS dep
            ON t.department_id = dep.department_id

        LEFT JOIN dw.dim_locations AS loc
            ON t.location_id = loc.location_id

        LEFT JOIN dw.dim_assets AS ast
            ON t.asset_id = ast.asset_id

    ) AS source

    ON target.ticket_id = source.ticket_id

    WHEN MATCHED THEN

        UPDATE SET
            target.ticket_number = source.ticket_number,
            target.date_key = source.date_key,
            target.user_key = source.user_key,
            target.agent_key = source.agent_key,
            target.category_key = source.category_key,
            target.department_key = source.department_key,
            target.location_key = source.location_key,
            target.asset_key = source.asset_key,

            target.priority = source.priority,
            target.status = source.status,
            target.created_at = source.created_at,
            target.resolved_at = source.resolved_at,
            target.resolution_hours = source.resolution_hours,
            target.satisfaction_score = source.satisfaction_score,
            target.sla_target_hours = source.sla_target_hours,
            target.sla_breached = source.sla_breached,
            target.sla_compliant = source.sla_compliant,
            target.sla_utilization = source.sla_utilization,
            target.backlog_flag = source.backlog_flag,
            target.high_priority_flag = source.high_priority_flag,
            target.resolution_bucket = source.resolution_bucket,
            target.is_weekend = source.is_weekend

    WHEN NOT MATCHED BY TARGET THEN

        INSERT
        (
            ticket_id,
            ticket_number,
            date_key,
            user_key,
            agent_key,
            category_key,
            department_key,
            location_key,
            asset_key,

            priority,
            status,
            created_at,
            resolved_at,
            resolution_hours,
            satisfaction_score,
            sla_target_hours,
            sla_breached,
            sla_compliant,
            sla_utilization,
            backlog_flag,
            high_priority_flag,
            resolution_bucket,
            is_weekend
        )

        VALUES
        (
            source.ticket_id,
            source.ticket_number,
            source.date_key,
            source.user_key,
            source.agent_key,
            source.category_key,
            source.department_key,
            source.location_key,
            source.asset_key,

            source.priority,
            source.status,
            source.created_at,
            source.resolved_at,
            source.resolution_hours,
            source.satisfaction_score,
            source.sla_target_hours,
            source.sla_breached,
            source.sla_compliant,
            source.sla_utilization,
            source.backlog_flag,
            source.high_priority_flag,
            source.resolution_bucket,
            source.is_weekend
        );

END;
GO