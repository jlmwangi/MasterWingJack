-- prepares mysql server for the project

CREATE DATABASE IF NOT EXISTS mwj_dev_db;

CREATE USER IF NOT EXISTS 'mwj_dev'@'localhost' IDENTIFIED BY 'mwj_dev_pwd';

GRANT ALL PRIVILEGES ON mwj_dev_db.* TO 'mwj_dev'@'localhost';

GRANT SELECT ON perfomance_schema.* TO 'mwj_dev'@'localhost';

FLUSH PRIVILEGES;
