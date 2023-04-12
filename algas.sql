ALTER USER 'root'@'localhost' IDENTIFIED BY '******';

DROP USER IF EXISTS 'urubu100' @'%';
CREATE USER IF NOT EXISTS 'urubu100' @'%' IDENTIFIED BY '******';
GRANT ALL PRIVILEGES ON `urubu100`.* TO `urubu100` @`%`;
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS 'grupo4';
USE 'grupo4';

CREATE TABLE IF NOT EXISTS `medidas` (
    id int PRIMARY KEY AUTO_INCREMENT,
    sensor VARCHAR(15),                      
    value  DOUBLE,                    
    ingestion_date  DATE 
);

CREATE TABLE IF NOT EXISTS `infos` (
    id int PRIMARY KEY AUTO_INCREMENT,
    time_taken DOUBLE,                      
    bytes_used  DOUBLE,                    
    cpu_used  DOUBLE,
    ram_used DOUBLE
);
