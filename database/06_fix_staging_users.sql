USE HelpDeskAnalytics;

DROP TABLE IF EXISTS stg.users;

CREATE TABLE stg.users
(
    user_id INT NOT NULL,
    user_name VARCHAR(150) NULL,
    email VARCHAR(255) NULL,
    department_id INT NULL,
    location_id INT NULL,
    status VARCHAR(50) NULL,
    job_title VARCHAR(100) NULL
);