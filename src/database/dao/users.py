# -*- coding: utf-8 -*-

def add(db, user):

    sql_statement = f"INSERT IGNORE INTO users (username, uid, ready, aware) VALUES " \
                    f"(\"{user.username}\", " \
                    f"\"{user.uid}\", " \
                    f"\"{int(user.ready)}\", " \
                    f"\"{int(user.aware)}\")"

    with db.cursor() as cursor:
        cursor.execute(sql_statement)
        db.commit()


def is_ready(connection, user):
    # TODO: method should be implemented

    sql_statement = f"SELECT uid FROM users WHERE username = \"{user}\""

    with connection.cursor() as cursor:
        cursor.execute(sql_statement)
        result = cursor.fetchall()
        return result


def set_ready(db, user):
    sql_statement = f"UPDATE users SET ready = \"{int(user.ready)}\" WHERE uid = \"{user.uid}\""
    with db.cursor() as cursor:
        cursor.execute(sql_statement)
        db.commit()


def get_users():
    # TODO: method should be implemented
    pass
