USE HelpDeskAnalytics;

/*FACT TICKETS*/
CREATE INDEX IX_fact_tickets_date ON dw.fact_tickets(date_key);
CREATE INDEX IX_fact_tickets_user ON dw.fact_tickets(user_key);
CREATE INDEX IX_fact_tickets_agent ON dw.fact_tickets(agent_key);
CREATE INDEX IX_fact_tickets_category ON dw.fact_tickets(category_key);
CREATE INDEX IX_fact_tickets_department ON dw.fact_tickets(department_key);
CREATE INDEX IX_fact_tickets_location ON dw.fact_tickets(location_key);
CREATE INDEX IX_fact_tickets_asset ON dw.fact_tickets(asset_key);
CREATE INDEX IX_fact_tickets_priority ON dw.fact_tickets(priority);
CREATE INDEX IX_fact_tickets_status ON dw.fact_tickets(status);
CREATE INDEX IX_fact_tickets_created_at ON dw.fact_tickets(created_at);

/*TICKETS EVENNTS*/
CREATE INDEX IX_ticket_events_ticket ON dw.fact_tickets_events(ticket_id);
CREATE INDEX IX_ticket_events_timestamp ON dw.fact_tickets_events(event_timestamp);