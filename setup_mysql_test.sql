-- prepares mysql server for the project

CREATE DATABASE IF NOT EXISTS mwj_test_db;

CREATE USER IF NOT EXISTS 'mwj_test'@'localhost' IDENTIFIED BY 'mwj_test_pwd';

GRANT ALL PRIVILEGES ON mwj_test_db.* TO 'mwj_test'@'localhost';

GRANT SELECT ON perfomance_schema.* TO 'mwj_test'@'localhost';

FLUSH PRIVILEGES;
