-- Create initial database tables
CREATE DATABASE if not exists coffee;
use coffee;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS meets;

CREATE TABLE IF NOT EXISTS users
(
    id         INT          NOT NULL AUTO_INCREMENT,
    username   VARCHAR(100) NOT NULL,
    uid        VARCHAR(100) NOT NULL,
    ready      BOOLEAN      NOT NULL,
    aware      BOOLEAN      NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY (uid)
);

CREATE TABLE IF NOT EXISTS meets
(
    id   INT NOT NULL AUTO_INCREMENT,
    season INT NOT NULL,
    uid1 INT NOT NULL,
    uid2 INT NOT NULL,
    PRIMARY KEY (`id`)
);