USE HelpDeskAnalytics;

/*FOREIGN KEY: USERS*/
ALTER TABLE dw.fact_tickets
ADD CONSTRAINT FK_fact_tickets_users 
FOREIGN KEY (user_key)
REFERENCES dw.dim_users(user_key);

/*FOREIGN KEY: AGENTS*/
ALTER TABLE dw.fact_tickets
ADD CONSTRAINT FK_fact_tickets_agents
FOREIGN KEY (agent_key)
REFERENCES dw.dim_agents(agent_key);

/*FOREIGN KEY: CATEGORIES*/
ALTER TABLE dw.fact_tickets
ADD CONSTRAINT FK_fact_tickets_categories
FOREIGN KEY (category_key)
REFERENCES dw.dim_categories(category_key);

/*FOREIGN KEY: CATEGORIES*/
ALTER TABLE dw.fact_tickets
ADD CONSTRAINT FK_fact_tickets_categories
FOREIGN KEY (category_key)
REFERENCES dw.dim_categories(category_key);

/*FOREIGN KEY: DEPARTMENTS*/
ALTER TABLE dw.fact_tickets
ADD CONSTRAINT FK_fact_tickets_departments
FOREIGN KEY (department_key)
REFERENCES dw.dim_departments(department_key);

/*FOREIGN KEY: LOCATIONS*/
ALTER TABLE dw.fact_tickets
ADD CONSTRAINT FK_fact_tickets_locations
FOREIGN KEY (location_key)
REFERENCES dw.dim_locations(location_key);

/*FOREIGN KEY: ASSETS*/
ALTER TABLE dw.fact_tickets
ADD CONSTRAINT FK_fact_tickets_assets
FOREIGN KEY (asset_key)
REFERENCES dw.dim_assets(asset_key);

/*FOREIGN KEY: DATE*/
ALTER TABLE dw.fact_tickets
ADD CONSTRAINT FK_fact_tickets_date
FOREIGN KEY (date_key)
REFERENCES dw.dim_date(date_key);
