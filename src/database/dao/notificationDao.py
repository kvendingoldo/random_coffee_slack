# -*- coding: utf-8 -*-

COLUMNS = ["info", "reminder", "feedback", "next_week"]


class NotificationDao:
    def __init__(self, connector):
        self.connector = connector

    def is_notified(self, uid, column):
        if column not in COLUMNS:
            raise ValueError(f"Wrong value for notification column name: {column}")

        sql_statement = f"SELECT {column} FROM notifications WHERE uid = \'{uid}\'"
        result = self.connector.get(sql_statement)

        if len(result) > 0:
            return bool(result[0][0])
        else:
            return False

    def change_column(self, uid, column, notified="1"):
        if column not in COLUMNS:
            raise ValueError(f"Wrong value for notification column name: {column}")

        sql_statement = f"SELECT {column} FROM notifications WHERE uid = \'{uid}\'"
        result = self.connector.get(sql_statement)

        if len(result) > 0:
            sql_statement = f"UPDATE notifications SET {column} = \'{notified}\' WHERE uid = \'{uid}\'"
        else:
            sql_statement = f"INSERT INTO notifications (uid, {column}) VALUES (\'{uid}\', \'{notified}\')"

        return self.connector.post(sql_statement)

    def change_all(self, uid, notified="1"):
        for column in COLUMNS:
            self.change_column(uid, column, notified)
