-- users
INSERT INTO user (id, username , pause_in_weeks, loc, meet_group) VALUES ('USR0', 'user0', 0, 'saratov', 'saratov');
INSERT INTO user (id, username , pause_in_weeks, loc, meet_group) VALUES ('USR1', 'user1', 0, 'us', 'us');
INSERT INTO user (id, username , pause_in_weeks, loc, meet_group) VALUES ('USR2', 'user2', 0, 'spb', 'us');

-- rating
INSERT INTO rating (uid1, uid2, value) VALUES ('USR0', 'USR1', 1.1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR0', 'USR2', 0.9);

INSERT INTO rating (uid1, uid2, value) VALUES ('USR1', 'USR0', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR1', 'USR2', 1);

INSERT INTO rating (uid1, uid2, value) VALUES ('USR2', 'USR0', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR2', 'USR1', 1);

-- meets
INSERT INTO meet (season, uid1, uid2, completed) VALUES ('202100', 'USR0', 'USR2', 1);
