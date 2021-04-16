# -*- coding: utf-8 -*-

class CMeets(object):
    def __init__(self, connector):
        self.connector = connector


    def add(self, user1, user2):
        sql_statement = f"INSERT IGNORE INTO meets (uid1, uid2) VALUES " \
                        f"(\'{user1.uid}\', " \
                        f"\'{user2.uid}\' "

        return self.connector.post(sql_statement)

    def get(self, user1, user2, season):
        sql_statement = f"SELECT * FROM meets WHERE season = \'{season}\' AND(uid1 = \'{user1}\' OR uid2 = \'{user2}\')"

        return self.connector.get(sql_statement)