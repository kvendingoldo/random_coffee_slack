use coffee;

ALTER TABLE meet
    ADD tmst_created datetime default CURRENT_TIMESTAMP null,
    ADD tmst_updated datetime                           null;

ALTER TABLE notification
    RENAME COLUMN time_created TO tmst_created,
    RENAME COLUMN time_updated TO tmst_updated;

ALTER TABLE rating
    ADD tmst_created datetime default CURRENT_TIMESTAMP null,
    ADD tmst_updated datetime                           null;

ALTER TABLE user
    ADD tmst_created datetime default CURRENT_TIMESTAMP null,
    ADD tmst_updated datetime                           null;
