# -*- coding: utf-8 -*-

import random

from loguru import logger

from utils import season
from database import exceptions


class MeetDao:
    def __init__(self, connector):
        self.connector = connector

    # todo
    def create(self, uids, config, type='random'):
        logger.info("Starting algorithm for create pairs")

        if type == 'random':
            self.__create_random(uids, config)

        logger.info("Algorithm for creating pairs has successfully completed")

    def __create_random(self, uids, config):
        season_cur_id = season.get()

        for_rand_distr = []

        while len(uids) >= 1:
            uid = uids[0]

            if len(uids) == 1:
                if not self.check_exist_by_id(uid, season_cur_id):
                    for_rand_distr.append(uid)
                break

            if self.check_exist_by_id(uid, season_cur_id):
                uids.remove(uid)
                continue

            sql_statement = f"SELECT AVAIL.uid " \
                            f"FROM (SELECT uid FROM users WHERE pause_in_weeks = '0' AND uid != '{uid}') as AVAIL " \
                            f"LEFT JOIN (" \
                            f"      SELECT uid2 AS uid" \
                            f"      FROM meets" \
                            f"      WHERE season = '{season_cur_id}'" \
                            f"      UNION" \
                            f"      SELECT uid1 AS uid" \
                            f"      FROM meets" \
                            f"      WHERE season = '{season_cur_id}') as BUSY " \
                            f"ON AVAIL.uid = BUSY.uid WHERE BUSY.uid is NULL ORDER BY RAND();"

            result = self.connector.get(sql_statement)

            if result:
                uid2 = result[0][0]

                if self.check_exist_by_ids(uid, uid2, season.get("previous")):
                    for_rand_distr.append(uid)
                else:
                    self.add_by_ids(uid, uid2, season_cur_id)
                    uids.remove(uid2)

                uids.remove(uid)

            else:
                if len(uids) > 0:
                    for_rand_distr.append(uid)
                    uids.remove(uid)

        if for_rand_distr:
            if (len(for_rand_distr) % 2) == 1:
                for_rand_distr.append(config["bot"]["additionalUsers"][0])

            while len(for_rand_distr) > 0:
                uid1 = for_rand_distr[0]
                # Pick up random uid except for uid1
                uid2 = random.choice(
                    [uid for uid in for_rand_distr if uid != uid1]
                )

                self.add_by_ids(uid1, uid2, season_cur_id)
                for_rand_distr.remove(uid1)
                for_rand_distr.remove(uid2)

    def add_by_ids(self, uid1, uid2, season_id="current"):
        if season_id == "current":
            season_id = season.get()

        sql_statement = "INSERT IGNORE INTO meets (season, uid1, uid2, completed) VALUES " \
                        f"('{season_id}', '{uid1}' , '{uid2}','0')"

        return self.connector.post(sql_statement)

    def delete_by_id(self, uid):
        sql_statement = f"DELETE FROM meets WHERE " \
                        f"uid1=\'{uid}\'"

        self.connector.post(sql_statement)

        sql_statement = f"UPDATE meets SET " \
                        f"uid2='deleted'" \
                        f"WHERE uid2=\'{uid}\'"

        self.connector.post(sql_statement)

        return True

    def get_uid2_by_id(self, season_id, uid):
        sql_statement = f"SELECT uid2 as uid FROM meets WHERE season = '{season_id}\' AND uid1 = '{uid}' " \
                        f"UNION " \
                        f"SELECT uid1 as uid FROM meets WHERE season = '{season_id}\' AND uid2 = '{uid}'"

        result = self.connector.get(sql_statement)

        if result:
            return result[0][0]
        else:
            pass
            #raise exceptions.NoResultFound

    def get_status_by_id(self, season_id, uid):
        sql_statement = f"SELECT completed FROM meets WHERE " \
                        f"(uid1 = '{uid}' OR uid2 = '{uid}') AND season = '{season_id}'"

        result = self.connector.get(sql_statement)

        if result:
            return bool(result[0][0])
        else:
            pass
            #raise exceptions.NoResultFound("")

    def check_exist_by_ids(self, uid1, uid2, season_id):
        sql_statement = f"SELECT season " \
                        f"FROM meets " \
                        f"WHERE uid1 = '{uid1}' AND uid2 = '{uid2}' AND season = '{season_id}' " \
                        f"UNION " \
                        f"SELECT season " \
                        f"FROM meets " \
                        f"WHERE uid1 = '{uid2}' AND uid2 = '{uid1}' AND season = '{season_id}'"

        result = self.connector.get(sql_statement)

        if result:
            return True
        else:
            return False

    def check_exist_by_id(self, uid, season_id):
        sql_statement = f"SELECT uid2 AS uid " \
                        f"FROM meets " \
                        f"WHERE uid1 = '{uid}' AND season = '{season_id}' " \
                        f"UNION " \
                        f"SELECT uid1 AS uid " \
                        f"FROM meets " \
                        f"WHERE uid2 = '{uid}' AND season = '{season_id}'"

        result = self.connector.get(sql_statement)

        if result:
            return True
        else:
            return False
