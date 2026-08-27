USE HelpDeskAnalytics;

DROP TABLE IF EXISTS stg.categories;

CREATE TABLE stg.categories
(
    category_id INT NOT NULL,
    category VARCHAR(100) NULL,
    subcategory VARCHAR(100) NULL
);