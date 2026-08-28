USE HelpDeskAnalytics;
GO

CREATE OR ALTER PROCEDURE dw.sp_load_dim_users
AS
BEGIN
    SET NOCOUNT ON;

    MERGE INTO dw.dim_users AS target

    USING
    (
        SELECT
            user_id,

            CAST(NULL AS VARCHAR(50)) AS employee_number,

            LEFT(
                user_name,
                CHARINDEX(' ', user_name + ' ') - 1
            ) AS first_name,

            LTRIM(
                SUBSTRING(
                    user_name,
                    CHARINDEX(' ', user_name + ' '),
                    LEN(user_name)
                )
            ) AS last_name,

            email,

            department_id,

            location_id,

            CAST(
                CASE
                    WHEN status = 'Activo' THEN 1
                    ELSE 0
                END
                AS BIT
            ) AS is_active,

            SYSDATETIME() AS created_at

        FROM stg.users

    ) AS source

    ON target.user_id = source.user_id

    WHEN MATCHED THEN

        UPDATE SET
            target.employee_number = source.employee_number,
            target.first_name = source.first_name,
            target.last_name = source.last_name,
            target.email = source.email,
            target.department_id = source.department_id,
            target.location_id = source.location_id,
            target.is_active = source.is_active

    WHEN NOT MATCHED BY TARGET THEN

        INSERT
        (
            user_id,
            employee_number,
            first_name,
            last_name,
            email,
            department_id,
            location_id,
            is_active,
            created_at
        )

        VALUES
        (
            source.user_id,
            source.employee_number,
            source.first_name,
            source.last_name,
            source.email,
            source.department_id,
            source.location_id,
            source.is_active,
            source.created_at
        );

END;
GO