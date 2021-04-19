# -*- coding: utf-8 -*-
import random

from entities import user
from random import randrange, shuffle


class UsersDAO(object):
    def __init__(self, connector):
        self.connector = connector

    def add(self, user):
        sql_statement = f"INSERT IGNORE INTO users (username, uid, loc, ready, aware) VALUES " \
                        f"(\'{user.username}\', " \
                        f"\'{user.uid}\', " \
                        f"\'{user.loc}\', " \
                        f"\'{int(user.ready)}\', " \
                        f"\'{int(user.aware)}\')"

        return self.connector.post(sql_statement)

    def is_new(self, uid):
        sql_statement = ""
        return self.connector.get(sql_statement)

    def is_ready(self, uid):
        sql_statement = f"SELECT ready FROM users WHERE username = \'{uid}\'"

        return self.connector.get(sql_statement)

    def set_ready(self, uid):
        sql_statement = f"UPDATE users SET ready = \'{int(uid.ready)}\' WHERE uid = \'{uid.uid}\'"
        return self.connector.post(sql_statement)

    def set_loc(self, uid):
        sql_statement = f"UPDATE users SET loc = \'{uid.loc}\' WHERE uid = \'{uid.uid}\'"
        return self.connector.post(sql_statement)

    def get_user(self, uid):
        sql_statement = f"SELECT * FROM users WHERE uid = \'{uid}\'"
        result = self.connector.get(sql_statement)
        print(result)
        if len(result) > 0:
            return user.User(
                username=result[0][1],
                uid=result[0][2],
                loc=result[0][3],
                ready=result[0][4],
                aware=result[0][5]
            )
        else:
            return False

    def list_all(self):
        users = []

        sql_statement = "SELECT * FROM users"
        result = self.connector.get(sql_statement)
        for row in result:
            users.append(
                user.User(username=row[1], uid=row[2], loc=row[3], ready=row[4], aware=row[5])
            )

        return users

    def ready_all(self):
        sql_statement = f"SELECT uid FROM users where ready = 1"
        ready = []
        result = self.connector.get(sql_statement)
        for id in result:
            ready.append(id[0])

        return ready
