-- Create initial database tables
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS meets;

CREATE TABLE IF NOT EXISTS users
(
    id         INT          NOT NULL AUTO_INCREMENT,
    username   VARCHAR(100) NOT NULL,
    name       VARCHAR(100) NOT NULL,
    channel_id VARCHAR(20)  NOT NULL,
    ready      BOOLEAN      NOT NULL,
    aware      BOOLEAN      NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY (username)
);

CREATE TABLE IF NOT EXISTS meets
(
    id   INT NOT NULL AUTO_INCREMENT,
    uid1 INT NOT NULL,
    uid2 INT NOT NULL,
    PRIMARY KEY (`id`)
);