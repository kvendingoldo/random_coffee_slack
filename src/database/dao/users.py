# -*- coding: utf-8 -*-
from src import entities


def add(connector, user):
    sql_statement = f"INSERT IGNORE INTO users (username, uid, ready, aware) VALUES " \
                    f"(\'{user.username}\', " \
                    f"\'{user.uid}\', " \
                    f"\'{int(user.ready)}\', " \
                    f"\'{int(user.aware)}\')"

    return connector.post(sql_statement)


def is_new(connector, uid):
    sql_statement = ""
    return connector.get(sql_statement)


def is_ready(connector, uid):
    sql_statement = f"SELECT ready FROM users WHERE username = \'{uid}\'"

    return connector.get(sql_statement)


def set_ready(connector, uid):
    sql_statement = f"UPDATE users SET ready = \'{int(uid.ready)}\' WHERE uid = \'{uid.uid}\'"
    return connector.post(sql_statement)


def get_user(connector, uid):
    sql_statement = f"SELECT * FROM users WHERE uid = \'{uid}\'"
    result = connector.get(sql_statement)

    return entities.user.User(username=result[1], uid=result[2], ready=result[3], aware=result[4])


def list_all(connector):
    users = []

    sql_statement = f"SELECT * FROM users"
    result = connector.get(sql_statement)
    for row in result:
        users.append(
            entities.user.User(username=row[1], uid=row[2], ready=row[3], aware=row[4])
        )

    return users
