# -*- coding: utf-8 -*-

import random

from loguru import logger

from contextlib import AbstractContextManager
from typing import Callable, Iterator, Mapping

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from utils import repo, season

from models.meet import Meet
from db.exceptions import MeetNotFoundError


class MeetRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def create(self, uids, additional_uids=None, type='random'):
        logger.info("Starting algorithm to create meets")

        if additional_uids is None:
            additional_uids = []
        if type == 'random':
            self.__create_random(uids, additional_uids)

        logger.info("Algorithm for creating pairs has successfully completed")

    def __create_random(self, uids, additional_users):
        season_id = season.get()

        for_rand_distr = []

        while len(uids) >= 1:
            cur_uid = uids[0]

            if self.check_exist(season_id, {"uid1": cur_uid}) or self.check_exist(season_id, {"uid2": cur_uid}):
                uids.remove(cur_uid)
                continue

            if len(uids) == 1:
                for_rand_distr.append(cur_uid)
                break

            with self.session_factory() as session:
                # take all meets in the current season
                meets = session.query(Meet).filter_by(season=season_id)

            # Take a shuffled list of available users who do not have a meet in the current season
            potential = []
            for uid in uids:
                if uid == cur_uid:
                    continue
                take = True
                for meet in meets:
                    if uid == meet.uid1 or uid == meet.uid2:
                        take = False
                        break
                if take:
                    potential.append(uid)

            random.shuffle(potential)

            if len(potential) > 0:
                pair_uid = potential[0]

                # NOTE: check that uid1 and uid2 didn't have a meet 1 & 2 weeks ago
                if self.check_exist(season.get("delta", 7), {"uid1": cur_uid, "uid2": pair_uid}) or \
                    self.check_exist(season.get("delta", 7), {"uid1": pair_uid, "uid2": cur_uid}) or \
                    self.check_exist(season.get("delta", 14), {"uid1": cur_uid, "uid2": pair_uid}) or \
                    self.check_exist(season.get("delta", 14), {"uid1": pair_uid, "uid2": cur_uid}):
                    for_rand_distr.append(cur_uid)
                else:
                    self.add(Meet(season=season_id, uid1=cur_uid, uid2=pair_uid))
                    uids.remove(pair_uid)
                    logger.info(f"Meet created for pair ({cur_uid}, {pair_uid})")
            else:
                logger.info(f"Meet can't be create for {cur_uid}; No potential users found")
                uids.remove(cur_uid)

        if for_rand_distr:
            while len(for_rand_distr) > 1:
                uid1 = for_rand_distr[0]

                # Pick up random uid except for uid1
                uid2 = random.choice(
                    [uid for uid in for_rand_distr if uid != uid1]
                )

                self.add(Meet(season=season_id, uid1=uid1, uid2=uid2))
                for_rand_distr.remove(uid1)
                for_rand_distr.remove(uid2)
                logger.info(f"Meet created for pair ({uid1}, {uid2})")

        if len(for_rand_distr) == 1:
            uid1 = for_rand_distr[0]
            if additional_users:
                uid2 = random.choice(additional_users)

                logger.info(f"Meet created for pair ({uid1}, {uid2})")
                self.add(Meet(season=season_id, uid1=uid1, uid2=uid2))
            else:
                logger.info(f"List of additional users is empty. Meet can not be created for user {uid1}")

    def check_exist(self, season, spec: Mapping = None):
        with self.session_factory() as session:
            meets = session.query(Meet).filter(season == season)
            if not meets:
                raise MeetNotFoundError("")

            if len(repo.filtration(spec, meets)) > 0:
                return True
            else:
                return False

    def add(self, meet: Meet) -> Meet:
        with self.session_factory() as session:
            session.add(meet)
            session.commit()
            session.refresh(meet)
            return meet

    def delete_all_by_uid(self, uid: str) -> None:
        with self.session_factory() as session:
            entities: Meet = session.query(Meet).filter(
                or_(Meet.uid1 == uid, Meet.uid2 == uid)
            )

            if not entities:
                raise MeetNotFoundError("")

            for entity in entities:
                session.delete(entity)

            session.commit()

    def list(self, spec: Mapping = None) -> Iterator[Meet]:
        with self.session_factory() as session:
            objs = session.query(Meet).all()

        return repo.filtration(spec, objs)
