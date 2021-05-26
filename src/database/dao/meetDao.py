# -*- coding: utf-8 -*-

from utils import season
from database import exceptions


class MeetDao:
    def __init__(self, connector):
        self.connector = connector

    def create(self):
        users = []

        season = season.get_current()

        for user in users:
            #     sql_statement = f"SELECT AVAIL.user" \
            #                     f"FROM (SELECT uid2 AS user FROM rating where uid1 = ? ORDER BY value DESC) AVAIL" \
            #
            #                     f"LEFT JOIN (" \
            #                     f"SELECT DISTINCT user" \
            #                     f"FROM (" \
            #                     f"SELECT uid2 AS user, season" \
            #                     f"FROM meets" \
            #                     f"WHERE uid1 = ?" \
            #                     f"UNION" \
            #
            #                     f"SELECT uid1 AS user, season" \
            #                     f"FROM meets" \
            #                     f"WHERE uid2 = ?" \
            #                     f") RES" \
            #                     f"WHERE season = ?" \
            #                     f") BUSY ON AVAIL.user = BUSY.user" \
            #                     f"WHERE BUSY.user IS null;"
            #     user2 = ""

            self.add(uid1, uid2)

        # TODO: kvendingoldo after implementation of DAO layer
        # while True:
        #     # make pairs
        #     # notify user
        #     print("pairs daemons")
        #
        #     sclient.chat_postMessage(channel="U01THB38EDV",
        #                              text="Hey!👋\n\n" \
        #                                   "This week your Random Coffee partner is @nickname!\n\n" \
        #                                   "Lucky you :)\n\n" \
        #                                   "Slack them now to set up a meeting."
        #                              )
        #     time.sleep(period)

    def add(self, uid1, uid2, season_id="current"):
        if season_id == "current":
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

        result = self.connector.get(sql_statement)

        if result:
            return result[0][0]
        else:
            raise exceptions.NoResultFound("")

    def get_status(self, season_id, uid):
        sql_statement = f"SELECT completed FROM meets WHERE (uid1 = \'{uid}\' OR uid2 = \'{uid}\') AND season = \'{season_id}\'"

        result = self.connector.get(sql_statement)

        if result:
            return bool(result[0][0])
        else:
            raise exceptions.NoResultFound("")
