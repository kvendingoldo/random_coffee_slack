-- Create initial database tables
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS meets;

CREATE TABLE IF NOT EXISTS users
(
    id          INT          NOT NULL AUTO_INCREMENT,
    uid         INT          NOT NULL,
    username    VARCHAR(100) NOT NULL,
    ready       BOOLEAN      NOT NULL,
    be_notified BOOLEAN      NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY (username)
);

CREATE TABLE IF NOT EXISTS meets
(
    id   INT NOT NULL AUTO_INCREMENT,
    uid1 INT NOT NULL,
    uid2 INT NOT NULL,
    week INT NOT NULL,
    PRIMARY KEY (`id`)
);