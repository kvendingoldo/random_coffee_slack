# -*- coding: utf-8 -*-

class RatingDao(object):
    def __init__(self, connector):
        self.connector = connector

    def init(self, user):
        result = self.connector.get("SELECT uid from users")

        for row in result:
            uid = row[1]
            if uid != user.uid:
                self.connector.post(f"INSERT INTO rating (uid1, uid2, value) VALUES (\'{uid}\', \'{user.uid}\', 1.0)")

    def change(self, user1, user2, delta):
        sql_statement = f"UPDATE rating SET value = \'{delta}\' WHERE uid1 = \'{user1.uid}\' AND uid2 =\'{user2.uid}\'"

        return self.connector.post(sql_statement)
