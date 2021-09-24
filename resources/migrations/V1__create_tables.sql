use coffee;

CREATE TABLE IF NOT EXISTS users
(
    id             VARCHAR(100) NOT NULL,
    username       VARCHAR(100) NOT NULL,
    loc            VARCHAR(100) NOT NULL,
    pause_in_weeks VARCHAR(3)   NOT NULL DEFAULT '0',
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS notifications
(
    id        INT     NOT NULL AUTO_INCREMENT,
    info      BOOLEAN NOT NULL DEFAULT false,
    reminder  BOOLEAN NOT NULL DEFAULT false,
    feedback  BOOLEAN NOT NULL DEFAULT false,
    next_week BOOLEAN NOT NULL DEFAULT false,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS meets
(
    id        INT          NOT NULL AUTO_INCREMENT,
    season    VARCHAR(100) NOT NULL,
    uid1      VARCHAR(100) NOT NULL,
    uid2      VARCHAR(100) NOT NULL,
    completed BOOLEAN      NOT NULL DEFAULT false,
    ntf_id    INT          NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (ntf_id)
        REFERENCES notifications (id)
        ON DELETE CASCADE,

    FOREIGN KEY (uid1)
        REFERENCES users (id)
        ON DELETE CASCADE,

    FOREIGN KEY (uid2)
        REFERENCES users (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rating
(
    id    INT          NOT NULL AUTO_INCREMENT,
    uid1  VARCHAR(100) NOT NULL,
    uid2  VARCHAR(100) NOT NULL,
    value DOUBLE       NOT NULL DEFAULT 1.0,
    PRIMARY KEY (id),
    FOREIGN KEY (uid1)
        REFERENCES users (id)
        ON DELETE CASCADE,

    FOREIGN KEY (uid2)
        REFERENCES users (id)
        ON DELETE CASCADE
);
