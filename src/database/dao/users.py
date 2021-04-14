# -*- coding: utf-8 -*-

def add(db, user):
    # TODO: method should be implemented

    sql_statement = "INSERT INTO users (uid, username, ready, be_notified) VALUES (%s, %s, True, True)"

    with db.cursor() as cursor:
        cursor.execute(sql_statement, user.username, user.uid, user.ready, user.be_notified)
        db.commit()


def is_ready(connection, user):
    # TODO: method should be implemented

    sql_statement = "SELECT ready FROM users WHERE uid = %s"

    with connection.cursor() as cursor:
        cursor.execute(sql_statement, user.uid)
        result = cursor.fetchall()
        return


def set_ready():
    # TODO: method should be implemented
    pass


def get_users():
    # TODO: method should be implemented
    pass
