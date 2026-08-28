USE HelpDeskAnalytics;
GO

CREATE OR ALTER PROCEDURE dw.sp_load_dim_categories
AS 
BEGIN
	SET NOCOUNT ON;
	MERGE INTO dw.dim_categories AS target
	USING(
	SELECT category_id,category AS category_name,
	subcategory AS subcategory_name
	FROM stg.categories
	) AS source
	ON target.category_id = source.category_id
	WHEN MATCHED THEN
		UPDATE SET
			target.category_name = source.category_name,
			target.subcategory_name = source.subcategory_name
	WHEN NOT MATCHED BY TARGET THEN
		INSERT(
			category_id,category_name,subcategory_name
		)
		VALUES(
			source.category_id,
			source.category_name,
			source.subcategory_name
		);
END;
GO