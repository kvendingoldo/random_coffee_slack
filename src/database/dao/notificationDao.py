# -*- coding: utf-8 -*-

class NotificationDao:
    def __init__(self, connector):
        self.connector = connector

    def is_notified(self, uid):
        sql_statement = f"SELECT status FROM notifications WHERE uid = \'{uid}\'"
        result = self.connector.get(sql_statement)

        if len(result) > 0:
            return bool(result[0][0])
        else:
            return False

    def change_status(self, uid, notified="1"):
        sql_statement = f"SELECT status FROM notifications WHERE uid = \'{uid}\'"
        result = self.connector.get(sql_statement)

        if len(result) > 0:
            sql_statement = f"UPDATE notifications SET status = \'{notified}\' WHERE uid = \'{uid}\'"
        else:
            sql_statement = f"INSERT INTO notifications (uid, status) VALUES (\'{uid}\', \'{notified}\')"

        return self.connector.post(sql_statement)

    def nullify_all(self):
        uids = self.connector.get(f"SELECT uid from users")
        for uid in uids:
            self.change_status(uid[0], "0")
