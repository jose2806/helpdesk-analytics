USE HelpDeskAnalytics;
GO

CREATE OR ALTER PROCEDURE dw.sp_load_dim_assets
AS
BEGIN
	SET NOCOUNT ON;
	MERGE INTO dw.dim_assets AS target
	USING(
		SELECT
			CAST(asset_id AS INT) AS asset_id,
			CAST(asset_tag AS VARCHAR(100)) AS asset_tag,
			CAST(asset_type AS VARCHAR(100)) AS asset_type,
			CAST(model AS VARCHAR(100)) AS model,
			CAST(serial_number AS VARCHAR(100)) AS serial_number,
			CAST(asset_status AS VARCHAR(50)) AS status ,
			TRY_CONVERT(DATE,purchase_date) AS purchase_date
			FROM stg.assets
	) AS source
	ON target.asset_id = source.asset_id
	WHEN MATCHED THEN
		UPDATE SET
			target.asset_tag = source.asset_tag,
            target.asset_type = source.asset_type,
            target.model = source.model,
            target.serial_number = source.serial_number,
            target.status = source.status,
            target.purchase_date = source.purchase_date
	WHEN NOT MATCHED BY TARGET THEN
		INSERT(
			asset_id,
            asset_tag,
            asset_type,
            model,
            serial_number,
            status,
            purchase_date
		)
		VALUES(
			source.asset_id,
            source.asset_tag,
            source.asset_type,
            source.model,
            source.serial_number,
            source.status,
            source.purchase_date
		);
END;
GO