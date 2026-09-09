USE HelpDeskAnalytics;
GO

CREATE OR ALTER PROCEDURE dw.sp_load_dim_departments
AS
BEGIN
	SET NOCOUNT ON;
	MERGE INTO dw.dim_departments AS target
	USING(
		SELECT
		department_id,
		department_name
		FROM stg.departments
	) AS source
	ON target.department_id = source.department_id
	WHEN MATCHED THEN
		UPDATE SET
			target.department_name = source.department_name
	WHEN NOT MATCHED BY TARGET THEN
		INSERT(
			department_id,
			department_name
		)
		VALUES(
			source.department_id,
			source.department_name
		);
END;
GO