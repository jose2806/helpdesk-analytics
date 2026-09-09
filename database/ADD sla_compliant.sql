use HelpDeskAnalytics;
IF COL_LENGTH('stg.tickets', 'sla_compliant') IS NULL
BEGIN
    ALTER TABLE stg.tickets
    ADD sla_compliant BIT NULL;
END;
GO