-- Create initial database tables
CREATE DATABASE if not exists coffee;
use coffee;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS meets;

CREATE TABLE IF NOT EXISTS users
(
    id             INT          NOT NULL AUTO_INCREMENT,
    username       VARCHAR(100) NOT NULL,
    uid            VARCHAR(100) NOT NULL,
    loc            VARCHAR(100) NOT NULL,
    ready          BOOLEAN      NOT NULL DEFAULT true,
    pause_in_weeks INT          NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    UNIQUE KEY (uid)
);

CREATE TABLE IF NOT EXISTS meets
(
    id        INT          NOT NULL AUTO_INCREMENT,
    season    VARCHAR(100) NOT NULL,
    uid1      VARCHAR(100) NOT NULL,
    uid2      VARCHAR(100) NOT NULL,
    completed BOOLEAN      NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS rating
(
    id    INT          NOT NULL AUTO_INCREMENT,
    uid1  VARCHAR(100) NOT NULL,
    uid2  VARCHAR(100) NOT NULL,
    value DOUBLE       NOT NULL,
    PRIMARY KEY (`id`)
);
