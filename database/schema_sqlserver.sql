/*
HelpDesk Analytics Platform
SQL Server / T-SQL
*/

IF DB_ID(N'HelpDesk') IS NULL
    CREATE DATABASE HelpDesk;
GO

USE HelpDesk;
GO

IF OBJECT_ID('dbo.ticket_events','U') IS NOT NULL DROP TABLE dbo.ticket_events;
IF OBJECT_ID('dbo.tickets','U') IS NOT NULL DROP TABLE dbo.tickets;
IF OBJECT_ID('dbo.assets','U') IS NOT NULL DROP TABLE dbo.assets;
IF OBJECT_ID('dbo.categories','U') IS NOT NULL DROP TABLE dbo.categories;
IF OBJECT_ID('dbo.users','U') IS NOT NULL DROP TABLE dbo.users;
IF OBJECT_ID('dbo.agents','U') IS NOT NULL DROP TABLE dbo.agents;
IF OBJECT_ID('dbo.locations','U') IS NOT NULL DROP TABLE dbo.locations;
IF OBJECT_ID('dbo.departments','U') IS NOT NULL DROP TABLE dbo.departments;
GO

CREATE TABLE dbo.departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);

CREATE TABLE dbo.locations (
    location_id INT PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL
);

CREATE TABLE dbo.agents (
    agent_id INT PRIMARY KEY,
    agent_name VARCHAR(120) NOT NULL,
    team VARCHAR(80),
    seniority VARCHAR(30)
);

CREATE TABLE dbo.users (
    user_id INT PRIMARY KEY,
    user_name VARCHAR(120) NOT NULL,
    email VARCHAR(180),
    department_id INT,
    location_id INT,
    status VARCHAR(30),
    job_title VARCHAR(100),
    FOREIGN KEY (department_id) REFERENCES dbo.departments(department_id),
    FOREIGN KEY (location_id) REFERENCES dbo.locations(location_id)
);

CREATE TABLE dbo.categories (
    category_id INT PRIMARY KEY,
    category VARCHAR(80),
    subcategory VARCHAR(100)
);

CREATE TABLE dbo.assets (
    asset_id INT PRIMARY KEY,
    asset_tag VARCHAR(40),
    asset_type VARCHAR(60),
    model VARCHAR(120),
    serial_number VARCHAR(80),
    asset_status VARCHAR(40),
    purchase_date DATE
);

CREATE TABLE dbo.tickets (
    ticket_id INT PRIMARY KEY,
    ticket_number VARCHAR(40) UNIQUE NOT NULL,
    created_at DATETIME2 NOT NULL,
    resolved_at DATETIME2 NULL,
    user_id INT NOT NULL,
    agent_id INT,
    category_id INT,
    location_id INT,
    asset_id INT NULL,
    priority VARCHAR(20),
    status VARCHAR(30),
    channel VARCHAR(30),
    impact VARCHAR(30),
    sla_target_hours DECIMAL(10,2),
    resolution_hours DECIMAL(10,2),
    sla_breached BIT,
    satisfaction_score TINYINT,
    FOREIGN KEY (user_id) REFERENCES dbo.users(user_id),
    FOREIGN KEY (agent_id) REFERENCES dbo.agents(agent_id),
    FOREIGN KEY (category_id) REFERENCES dbo.categories(category_id),
    FOREIGN KEY (location_id) REFERENCES dbo.locations(location_id),
    FOREIGN KEY (asset_id) REFERENCES dbo.assets(asset_id)
);

CREATE TABLE dbo.ticket_events (
    event_id INT PRIMARY KEY,
    ticket_id INT NOT NULL,
    event_at DATETIME2 NOT NULL,
    event_type VARCHAR(50),
    agent_id INT,
    source VARCHAR(30),
    FOREIGN KEY (ticket_id) REFERENCES dbo.tickets(ticket_id),
    FOREIGN KEY (agent_id) REFERENCES dbo.agents(agent_id)
);
GO

CREATE INDEX IX_tickets_created_at ON dbo.tickets(created_at);
CREATE INDEX IX_tickets_status ON dbo.tickets(status);
CREATE INDEX IX_tickets_agent_id ON dbo.tickets(agent_id);
CREATE INDEX IX_tickets_category_id ON dbo.tickets(category_id);
CREATE INDEX IX_ticket_events_ticket_id ON dbo.ticket_events(ticket_id);
GO
