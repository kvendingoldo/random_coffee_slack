# -*- coding: utf-8 -*-

import random

from loguru import logger

from utils import season
from database import exceptions


class MeetDao:
    def __init__(self, connector):
        self.connector = connector

    def create(self, uids, config, type='random'):
        logger.info("Starting algorithm for create pairs")

        if type == 'random':
            self.__create_random(uids, config)
        elif type == 'rating_based':
            self.__create_based_on_rating(uids, config)

        logger.info("Algorithm for creating pairs has successfully completed")

    def __create_for_list(self, users, config, season_id):
        if users:
            if (len(users) % 2) == 1:
                users.append(config["bot"]["additionalUsers"][0])

            for uid in users:
                uid_pair = random.choice(users)

                self.add(uid, uid_pair, season_id)

                users.remove(uid)
                users.remove(uid_pair)

    def __create_random(self, uids, config):
        season_cur_id = season.get_current()
        print(season_cur_id)
        season_prev_id = season.get_previous()

        for_rand_distr = []

        for uid in uids:
            if self.check_exist(uid, season_cur_id):
                continue

            print(uid)
            print("===")

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
                            f"ON AVAIL.uid = BUSY.uid WHERE BUSY.uid is NULL;"

            result = self.connector.get(sql_statement)

            print(result)

            # check it
            had_meet_on_prev_week = False
            if had_meet_on_prev_week:
                for_rand_distr.append(uid)
                continue

            if result:
                self.add(uid, result[0][0], season_cur_id)

                print(uid)
                print(result[0][0])

                uids.remove(uid)
                uids.remove(result[0][0])
            else:
                for_rand_distr.append(uid)

        self.__create_for_list(for_rand_distr, config, season_cur_id)

    def add(self, uid1, uid2, season_id="current"):
        if season_id == "current":
            season_id = season.get_current()

        sql_statement = "INSERT IGNORE INTO meets (season, uid1, uid2, completed) VALUES " \
                        f"(\'{season_id}\', " \
                        f"\'{uid1}\'," \
                        f"\'{uid2}\'," \
                        f"\'0\')"

        return self.connector.post(sql_statement)

    def delete(self, uid):
        sql_statement = f"DELETE FROM meets WHERE " \
                        f"uid1=\'{uid}\'"

        self.connector.post(sql_statement)

        sql_statement = f"UPDATE meets SET " \
                        f"uid2='deleted'" \
                        f"WHERE uid2=\'{uid}\'"

        self.connector.post(sql_statement)

        return True

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

    def check_exist(self, uid, season_id):

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
