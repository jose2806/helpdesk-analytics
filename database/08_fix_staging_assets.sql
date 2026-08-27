USE HelpDeskAnalytics;

DROP TABLE IF EXISTS stg.assets;

CREATE TABLE stg.assets
(
    asset_id INT NOT NULL,
    asset_tag VARCHAR(100) NULL,
    asset_type VARCHAR(100) NULL,
    model VARCHAR(150) NULL,
    serial_number VARCHAR(100) NULL,
    asset_status VARCHAR(50) NULL,
    purchase_date DATE NULL
);