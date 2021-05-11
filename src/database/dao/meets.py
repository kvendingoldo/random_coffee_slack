# -*- coding: utf-8 -*-

from utils import season


class MeetsDao(object):
    def __init__(self, connector):
        self.connector = connector

    def add(self, uid1, uid2):
        season_id = season.get_current()

        sql_statement = "INSERT IGNORE INTO meets (season, uid1, uid2) VALUES " \
                        f"(\'{uid1}\', " \
                        f"\'{uid2}\'" \
                        f"\'{season_id}\')"

        return self.connector.post(sql_statement)

    def get_partner_uid(self, season_id, uid):
        sql_statement = f"SELECT uid2 as uid FROM meets WHERE season = \'{season_id}\' AND uid1 = \'{uid}\' " \
                        f"UNION " \
                        f"SELECT uid1 as uid FROM meets WHERE season = \'{season_id}\' AND uid2 = \'{uid}\'"

        # TODO: check exception
        return self.connector.get(sql_statement)[0][0]
