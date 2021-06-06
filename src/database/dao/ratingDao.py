# -*- coding: utf-8 -*-


class RatingDao:
    def __init__(self, connector):
        self.connector = connector

    def add_by_id(self, uid):
        users = self.connector.get(f"SELECT uid from users WHERE uid != '{uid}'")
        for user in users:
            uid2 = user[0]

            self.connector.post(
                f"INSERT INTO rating (uid1, uid2, value) VALUES (\'{uid}\', \'{uid2}\', 1.0)"
            )

            self.connector.post(
                f"INSERT INTO rating (uid1, uid2, value) VALUES (\'{uid2}\', \'{uid}\', 1.0)"
            )

    def delete_by_id(self, uid):
        sql_statement = f"DELETE FROM rating WHERE " \
                        f"uid1=\'{uid}\' OR uid2=\'{uid}\'"

        return self.connector.post(sql_statement)

    def change_by_ids(self, uid1, uid2, delta):
        sql_statement = f"SELECT value FROM rating WHERE uid1 = \'{uid1}\' AND uid2 =\'{uid2}\'"

        result = self.connector.get(sql_statement)

        if result:
            cur_rating = float(result[0][0])
        else:
            cur_rating = 1.0

        new_rating = cur_rating + delta

        sql_statement = f"UPDATE rating SET value = \'{new_rating}\' WHERE uid1 = \'{uid1}\' AND uid2 =\'{uid2}\'"

        return self.connector.post(sql_statement)
