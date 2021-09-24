use coffee;

DROP TRIGGER clean_notifications;

CREATE TRIGGER clean_notifications
    AFTER DELETE
    on meets
    FOR EACH ROW
BEGIN
    DELETE
    FROM notifications
    WHERE notifications.id = old.ntf_id;
END
