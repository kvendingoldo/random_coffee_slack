# -*- coding: utf-8 -*-

from entities import user


class UserDAO:
    def __init__(self, connector):
        self.connector = connector

    def add(self, user):
        sql_statement = f"INSERT IGNORE INTO users (username, uid, loc, ready, pause_in_weeks) VALUES " \
                        f"(\'{user.username}\', " \
                        f"\'{user.uid}\', " \
                        f"\'{user.loc}\', " \
                        f"\'{int(user.ready)}\', " \
                        f"\'{int(user.pause_in_weeks)}\')"

        return self.connector.post(sql_statement)

    def update(self, user):
        sql_statement = f"UPDATE users SET " \
                        f"username=\'{user.username}\'," \
                        f"uid=\'{user.uid}\'," \
                        f"loc=\'{user.loc}\'," \
                        f"ready=\'{int(user.ready)}\'," \
                        f"pause_in_weeks=\'{int(user.pause_in_weeks)}\'" \
                        f"WHERE uid = \'{user.uid}\'"

        return self.connector.post(sql_statement)

    def is_ready(self, uid):
        sql_statement = f"SELECT ready FROM users WHERE username = \'{uid}\'"

        return self.connector.get(sql_statement)

    def set_unready(self, uid):
        sql_statement = f"UPDATE users SET ready = '0' WHERE uid = \'{uid}\'"
        return self.connector.post(sql_statement)

    def set_ready(self, uid):
        sql_statement = f"UPDATE users SET ready = '1' WHERE uid = \'{uid}\'"
        return self.connector.post(sql_statement)

    def set_loc(self, user):
        sql_statement = f"UPDATE users SET loc = \'{user.loc}\' WHERE uid = \'{user.uid}\'"
        return self.connector.post(sql_statement)

    def set_pause(self, user):
        sql_statement = f"UPDATE users SET pause_in_weeks = \'{user.pause_in_weeks}\' WHERE uid = \'{user.uid}\'"
        return self.connector.post(sql_statement)

    def get_user(self, uid):
        sql_statement = f"SELECT * FROM users WHERE uid = \'{uid}\'"
        result = self.connector.get(sql_statement)
        if len(result) > 0:
            return user.User(
                username=result[0][1],
                uid=result[0][2],
                loc=result[0][3],
                ready=result[0][4],
                pause_in_weeks=result[0][5]
            )
        else:
            return False

    def list(self):
        users = []

        sql_statement = "SELECT * FROM users"
        result = self.connector.get(sql_statement)
        for row in result:
            users.append(
                user.User(username=row[1], uid=row[2], loc=row[3], ready=row[4], pause_in_weeks=row[5])
            )

        return users

    def decrement_users_pause(self, decrement):
        users = self.list()

        for user in users:
            user.pause_in_weeks = user.pause_in_weeks - decrement
            self.update(user)
