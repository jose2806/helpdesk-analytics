USE HelpDeskAnalytics;
GO

IF NOT EXISTS(
  SELECT * FROM sys.schemas WHERE name = 'stg'
)
BEGIN
  EXEC('CREATE SCHEMA stg');
END;
GO

IF NOT EXISTS(
  SELECT * FROM sys.schemas WHERE name = 'dw'
)
BEGIN
  EXEC('CREATE SCHEMA dw');
END;
GO

CREATE TABLE dw.dim_users(
  user_key INT IDENTITY(1,1) NOT NULL,
  user_id INT NOT NULL,
  employee_number VARCHAR(50) NULL,
  first_name VARCHAR(100) NULL,
  last_name VARCHAR(100) NULL,
  email VARCHAR(255) NULL,
  department_id INT NULL,
  location_id INT NULL,
  is_active BIT NOT NULL DEFAULT 1,
  created_at DATETIME2 NULL,
  CONSTRAINT PK_dim_users PRIMARY KEY (user_key)
);
GO

CREATE TABLE dw.dim_agents(
  agent_key INT IDENTITY(1,1) NOT NULL,
  agent_id INT NOT NULL,
  agent_name VARCHAR(150) NOT NULL,
  team VARCHAR(100) NULL,
  seniority VARCHAR(50) NULL,
  is_active BIT NOT NULL DEFAULT 1,
  CONSTRAINT PK_dim_agents PRIMARY KEY (agent_key)
);
GO

CREATE TABLE dw.dim_categories(
  category_key INT IDENTITY(1,1) NOT NULL,
  category_id INT NOT NULL,
  category_name VARCHAR(100) NOT NULL,
  subcategory_name VARCHAR(100) NULL,
  CONSTRAINT PK_dim_categories PRIMARY KEY (category_key)
);
GO

CREATE TABLE dw.dim_departments(
  department_key INT IDENTITY(1,1) NOT NULL,
  department_id INT NOT NULL,
  department_name VARCHAR(150) NOT NULL,
  CONSTRAINT PK_dim_departments PRIMARY KEY (department_key)
);
GO

CREATE TABLE dw.dim_locations(
  location_key INT IDENTITY(1,1) NOT NULL,
  location_id INT NOT NULL,
  location_name VARCHAR(150) NOT NULL,
  city VARCHAR(100) NULL,
  country VARCHAR(100) NULL,
  CONSTRAINT PK_dim_locations PRIMARY KEY (location_key)
);
GO

CREATE TABLE dw.dim_assets(
  asset_key INT IDENTITY(1,1) NOT NULL,
  asset_id INT NOT NULL,
  asset_tag VARCHAR(100) NULL,
  asset_type VARCHAR(100) NULL,
  manufacturer VARCHAR(100) NULL,
  model VARCHAR(100) NULL,
  status VARCHAR(50) NULL,
  CONSTRAINT PK_dim_assets PRIMARY KEY (asset_key)
);
GO

CREATE TABLE dw.dim_date(
  date_key INT NOT NULL,
  full_date DATE NOT NULL,
  year_number INT NOT NULL,
  quarter_number INT NOT NULL,
  month_number INT NOT NULL,
  month_name VARCHAR(20) NOT NULL,
  week_number INT NOT NULL,
  day_number INT NOT NULL,
  day_name VARCHAR(20) NOT NULL,
  is_weekend BIT NOT NULL,
  CONSTRAINT PK_dim_date PRIMARY KEY (date_key)
);
GO

CREATE TABLE dw.fact_tickets(
  ticket_key BIGINT IDENTITY(1,1) NOT NULL,
  ticket_id INT NOT NULL,
  ticket_number VARCHAR(50) NOT NULL,
  date_key INT NOT NULL,
  user_key INT NOT NULL,
  agent_key INT NOT NULL,
  category_key INT NOT NULL,
  department_key INT NULL,
  location_key INT NULL,
  asset_key INT NULL,
  priority VARCHAR(20) NOT NULL,
  status VARCHAR(50) NOT NULL,
  created_at DATETIME2 NOT NULL,
  resolved_at DATETIME2 NULL,
  resolution_hours DECIMAL(10,2) NULL,
  satisfaction_score DECIMAL(3,2) NULL,
  sla_target_hours DECIMAL(10,2) NULL,
  sla_breached BIT NOT NULL,
  sla_utilization DECIMAL(10,4) NULL,
  backlog_flag BIT NOT NULL,
  high_priority_flag BIT NOT NULL,
  resolution_bucket VARCHAR(20) NULL,
  is_weekend BIT NOT NULL,
  CONSTRAINT PK_fact_tickets PRIMARY KEY (ticket_key)
);
GO

CREATE TABLE dw.fact_tickets_events(
  event_key BIGINT IDENTITY(1,1) NOT NULL,
  ticket_id INT NOT NULL,
  event_type VARCHAR(100) NOT NULL,
  event_timestamp DATETIME2 NOT NULL,
  agent_id INT NULL,
  previous_status VARCHAR(50) NULL,
  new_status VARCHAR(50) NULL,
  event_duration_minutes INT NULL,
  CONSTRAINT PK_fact_ticket_events PRIMARY KEY (event_key)
);
GO