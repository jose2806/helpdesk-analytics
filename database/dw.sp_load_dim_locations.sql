USE HelpDeskAnalytics;
GO

CREATE OR ALTER PROCEDURE dw.sp_load_dim_locations
AS
BEGIN
	SET NOCOUNT ON;
	MERGE INTO dw.dim_locations AS target
	USING(
		SELECT location_id,location_name,
		location_name AS city,country
		FROM stg.locations
	) AS source
	ON target.location_id = source.location_id
	WHEN MATCHED THEN
		UPDATE SET
			target.location_name = source.location_name,
			target.city = source.city,
			target.country = source.country
	WHEN NOT MATCHED BY TARGET THEN
		INSERT(
			location_id,
			location_name,
			city,
			country
		)
		VALUES
		(
			source.location_id,
			source.location_name,
			source.city,
			source.country
		);
END;
GO