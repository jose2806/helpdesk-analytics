IF NOT EXISTS(
  SELECT name 
  From sys.databases 
  WHERE name = 'HelpDeskAnalytics'
)
BEGIN
CREATE DATABASE HelpDeskAnalytics;
END;
GO