USE HelpDeskAnalytics;
GO

CREATE OR ALTER PROCEDURE dw.sp_load_dim_agents
AS
BEGIN
	SET NOCOUNT ON;
	MERGE INTO dw.dim_agents AS target
	USING(
		SELECT  agent_id,agent_name,team,seniority,
		CAST(1 AS BIT) AS is_active
		FROM stg.agents	
	) AS source
	ON target.agent_id = source.agent_id
	WHEN MATCHED THEN
		UPDATE SET
			target.agent_name = source.agent_name,
			target.team = source.team,
			target.seniority = source.seniority,
			target.is_active = source.is_active
	WHEN NOT MATCHED BY TARGET THEN
		INSERT(
			agent_id,agent_name,team,seniority,is_active
			)
		VALUES(
			source.agent_id,
			source.agent_name,
			source.team,
			source.seniority,
			source.is_active
		);
END;
GO