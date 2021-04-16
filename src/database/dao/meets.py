# -*- coding: utf-8 -*-

def add_meet(connector, user1, user2):
    sql_statement = f"INSERT IGNORE INTO meets (uid1, uid2) VALUES " \
                    f"(\"{user1.uid}\", " \
                    f"\"{user2.uid}\" "

    return connector.post(sql_statement)

def get_meet(connector, user1, user2, season):
    sql_statement = f"SELECT * FROM users WHERE season = \"{season}\" AND(uid1 = \"{user1}\" OR uid2 = \"{user2}\")"

    return connector.get(sql_statement)