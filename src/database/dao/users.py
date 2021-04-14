# -*- coding: utf-8 -*-


def add(connection, user):
    sql_statement = "INSERT INTO users (uid, username, ready, be_notified) VALUES (%s, %s, True, True)"

    with connection.cursor() as cursor:
        cursor.execute(sql_statement, user.username, user.uid, user.ready, user.be_notified)
        connection.commit()


def is_ready(connection, user):
    sql_statement = "SELECT ready FROM users WHERE uid = %s"

    with connection.cursor() as cursor:
        cursor.execute(sql_statement, user.uid)

        result = cursor.fetchall()

        return


def set_ready():
    pass


def get_users():
    pass
