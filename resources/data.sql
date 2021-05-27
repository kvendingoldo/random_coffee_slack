-- users
INSERT INTO users (username, uid, loc, ready, pause_in_weeks) VALUES ('user0', 'USR0', 'saratov', 1, 0);
INSERT INTO users (username, uid, loc, ready, pause_in_weeks) VALUES ('user1', 'USR1', 'saratov', 1, 0);
INSERT INTO users (username, uid, loc, ready, pause_in_weeks) VALUES ('user2', 'USR2', 'saratov', 1, 1);
INSERT INTO users (username, uid, loc, ready, pause_in_weeks) VALUES ('user3', 'USR3', 'saratov', 1, 4);
INSERT INTO users (username, uid, loc, ready, pause_in_weeks) VALUES ('user4', 'USR4', 'spb', 1, 0);
INSERT INTO users (username, uid, loc, ready, pause_in_weeks) VALUES ('user5', 'USR5', 'spb', 1, 0);
INSERT INTO users (username, uid, loc, ready, pause_in_weeks) VALUES ('user6', 'USR6', 'spb', 1, 1);
INSERT INTO users (username, uid, loc, ready, pause_in_weeks) VALUES ('user7', 'USR7', 'spb', 1, 4);
-- meets
INSERT INTO meets (season, uid1, uid2, completed) VALUES ('202120', 'USR0', 'USR1', 1);
INSERT INTO meets (season, uid1, uid2, completed) VALUES ('202120', 'USR4', 'USR5', 1);

INSERT INTO meets (season, uid1, uid2, completed) VALUES ('202119', 'USR0', 'USR2', 1);
INSERT INTO meets (season, uid1, uid2, completed) VALUES ('202119', 'USR1', 'USR4', 1);
INSERT INTO meets (season, uid1, uid2, completed) VALUES ('202119', 'USR5', 'USR6', 1);

-- rating
INSERT INTO rating (uid1, uid2, value) VALUES ('USR0', 'USR1', 1.1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR0', 'USR2', 0.9);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR0', 'USR3', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR0', 'USR4', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR0', 'USR5', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR0', 'USR6', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR0', 'USR7', 1);

INSERT INTO rating (uid1, uid2, value) VALUES ('USR1', 'USR0', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR1', 'USR2', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR1', 'USR3', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR1', 'USR4', 1.1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR1', 'USR5', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR1', 'USR6', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR1', 'USR7', 1);

INSERT INTO rating (uid1, uid2, value) VALUES ('USR2', 'USR0', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR2', 'USR1', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR2', 'USR3', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR2', 'USR4', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR2', 'USR5', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR2', 'USR6', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR2', 'USR7', 1);

INSERT INTO rating (uid1, uid2, value) VALUES ('USR3', 'USR0', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR3', 'USR1', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR3', 'USR2', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR3', 'USR4', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR3', 'USR5', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR3', 'USR6', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR3', 'USR7', 1);

INSERT INTO rating (uid1, uid2, value) VALUES ('USR4', 'USR0', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR4', 'USR1', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR4', 'USR2', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR4', 'USR3', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR4', 'USR5', 0.9);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR4', 'USR6', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR4', 'USR7', 1);

INSERT INTO rating (uid1, uid2, value) VALUES ('USR5', 'USR0', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR5', 'USR1', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR5', 'USR2', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR5', 'USR3', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR5', 'USR4', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR5', 'USR6', 1.1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR5', 'USR7', 1);

INSERT INTO rating (uid1, uid2, value) VALUES ('USR6', 'USR0', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR6', 'USR1', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR6', 'USR2', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR6', 'USR3', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR6', 'USR4', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR6', 'USR5', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR6', 'USR7', 1);

INSERT INTO rating (uid1, uid2, value) VALUES ('USR7', 'USR0', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR7', 'USR1', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR7', 'USR2', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR7', 'USR3', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR7', 'USR4', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR7', 'USR5', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR7', 'USR6', 1);
