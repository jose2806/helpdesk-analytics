USE HelpDeskAnalytics;

CREATE TABLE stg.tickets
(
    ticket_id INT NOT NULL,
    ticket_number VARCHAR(50) NULL,
    user_id INT NULL,
    agent_id INT NULL,
    category_id INT NULL,
    department_id INT NULL,
    location_id INT NULL,
    asset_id INT NULL,
    priority VARCHAR(20) NULL,
    status VARCHAR(50) NULL,
    created_at DATETIME2 NULL,
    resolved_at DATETIME2 NULL,
    resolution_hours DECIMAL(10,2) NULL,
    satisfaction_score DECIMAL(3,2) NULL,
    sla_target_hours DECIMAL(10,2) NULL,
    sla_breached BIT NULL,
    sla_utilization DECIMAL(10,4) NULL,
    backlog_flag BIT NULL,
    high_priority_flag BIT NULL,
    resolution_bucket VARCHAR(20) NULL,
    is_weekend BIT NULL
);


CREATE TABLE stg.users
(
    user_id INT NOT NULL,
    employee_number VARCHAR(50) NULL,
    first_name VARCHAR(100) NULL,
    last_name VARCHAR(100) NULL,
    email VARCHAR(255) NULL,
    department_id INT NULL,
    location_id INT NULL,
    is_active BIT NULL,
    created_at DATETIME2 NULL
);


CREATE TABLE stg.agents
(
    agent_id INT NOT NULL,
    agent_name VARCHAR(150) NULL,
    team VARCHAR(100) NULL,
    seniority VARCHAR(50) NULL,
    is_active BIT NULL
);


CREATE TABLE stg.categories
(
    category_id INT NOT NULL,
    category_name VARCHAR(100) NULL,
    subcategory_name VARCHAR(100) NULL
);


CREATE TABLE stg.departments
(
    department_id INT NOT NULL,
    department_name VARCHAR(150) NULL
);


CREATE TABLE stg.locations
(
    location_id INT NOT NULL,
    location_name VARCHAR(150) NULL,
    city VARCHAR(100) NULL,
    country VARCHAR(100) NULL
);


CREATE TABLE stg.assets
(
    asset_id INT NOT NULL,
    asset_tag VARCHAR(100) NULL,
    asset_type VARCHAR(100) NULL,
    manufacturer VARCHAR(100) NULL,
    model VARCHAR(100) NULL,
    status VARCHAR(50) NULL
);


CREATE TABLE stg.ticket_events
(
    ticket_id INT NOT NULL,
    event_type VARCHAR(100) NULL,
    event_timestamp DATETIME2 NULL,
    agent_id INT NULL,
    previous_status VARCHAR(50) NULL,
    new_status VARCHAR(50) NULL,
    event_duration_minutes INT NULL
);