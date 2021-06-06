# -*- coding: utf-8 -*-

from entities import user
from database import exceptions


class UserDAO:
    def __init__(self, connector):
        self.connector = connector

    def add(self, user):
        sql_statement = f"INSERT IGNORE INTO users (username, uid, loc, pause_in_weeks) VALUES " \
                        f"(\'{user.username}\'," \
                        f"\'{user.uid}\'," \
                        f"\'{user.loc}\'," \
                        f"\'{user.pause_in_weeks}\')"

        return self.connector.post(sql_statement)

    def delete_by_id(self, uid):
        sql_statement = f"DELETE FROM users WHERE " \
                        f"uid=\'{uid}\'"

        return self.connector.post(sql_statement)

    def update(self, user):
        sql_statement = f"UPDATE users SET " \
                        f"username=\'{user.username}\'," \
                        f"uid=\'{user.uid}\'," \
                        f"loc=\'{user.loc}\'," \
                        f"pause_in_weeks=\'{user.pause_in_weeks}\'" \
                        f"WHERE uid = \'{user.uid}\'"

        return self.connector.post(sql_statement)

    def get_by_id(self, uid):
        sql_statement = f"SELECT * FROM users WHERE uid = \'{uid}\'"
        result = self.connector.get(sql_statement)
        if len(result) > 0:
            return user.User(
                username=result[0][1],
                uid=result[0][2],
                loc=result[0][3],
                pause_in_weeks=result[0][4]
            )
        else:
            raise exceptions.NoResultFound

    def list(self, only_available=False):
        sql_statement = "SELECT * FROM users"

        if only_available:
            sql_statement += " WHERE pause_in_weeks = '0'"

        result = self.connector.get(sql_statement)
        if len(result) > 0:
            users = []
            for row in result:
                users.append(user.User(username=row[1], uid=row[2], loc=row[3], pause_in_weeks=row[4]))
            return users
        else:
            raise exceptions.NoResultFound

    def list_ids(self, only_available=False):
        sql_statement = "SELECT * FROM users"
        if only_available:
            sql_statement += " WHERE pause_in_weeks = '0'"

        result = self.connector.get(sql_statement)
        if len(result) > 0:
            ids = []
            for row in result:
                ids.append(row[2])

            return ids
        else:
            raise exceptions.NoResultFound

    def decrement_users_pause(self, decrement):
        users = self.list()

        for user in users:
            user.pause_in_weeks = str(int(user.pause_in_weeks) - decrement)
            self.update(user)
