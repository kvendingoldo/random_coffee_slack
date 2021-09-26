-- users
INSERT INTO user (id, username , loc, pause_in_weeks) VALUES ('USR0', 'user0', 'saratov', 0);
INSERT INTO user (id, username , loc, pause_in_weeks) VALUES ('USR1', 'user1', 'us', 0);
INSERT INTO user (id, username , loc, pause_in_weeks) VALUES ('USR2', 'user2', 'spb', 0);

-- rating
INSERT INTO rating (uid1, uid2, value) VALUES ('USR0', 'USR1', 1.1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR0', 'USR2', 0.9);

INSERT INTO rating (uid1, uid2, value) VALUES ('USR1', 'USR0', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR1', 'USR2', 1);

INSERT INTO rating (uid1, uid2, value) VALUES ('USR2', 'USR0', 1);
INSERT INTO rating (uid1, uid2, value) VALUES ('USR2', 'USR1', 1);

-- meets
INSERT INTO meet (season, uid1, uid2, completed) VALUES ('202100', 'USR0', 'USR2', 1);

-- notification
INSERT INTO notification (id, info, reminder, feedback, next_week, meet_id) VALUES ('HASH0', 0, 0, 0, 0, 1);
INSERT INTO notification (id, info, reminder, feedback, next_week, meet_id) VALUES ('HASH1', 0, 0, 0, 0, 2);
INSERT INTO notification (id, info, reminder, feedback, next_week, meet_id) VALUES ('HASH2', 0, 0, 0, 0, 3);
