# -*- coding: utf-8 -*-

import random

from contextlib import AbstractContextManager
from typing import Callable, Iterator, Mapping

from sqlalchemy.orm import Session

from utils import filter, season

from models.meet import Meet
from database.exceptions import MeetNotFoundError


class MeetRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def create(self, users, config, type='random'):
        # logger.info("Starting algorithm for create pairs")

        if type == 'random':
            self.__create_random(users, config)

        # logger.info("Algorithm for creating pairs has successfully completed")

    def __check_exist(self, season, spec: Mapping = None):
        pass

    def __create_random(self, users, config):
        season = season.get()

        for_rand_distr = []

        while len(users) >= 1:
            cur_user = users[0]

            # if len(uids) == 1:
            #     if not self.check_exist_by_id(uid, season_id):
            #         for_rand_distr.append(uid)
            #     break

            if self.__check_exist(cur_user, season):
                users.remove(cur_user)
                continue

            with self.session_factory() as session:
                # список всех у кого есть мит uid1, uid2
                meets = session.query(Meet).filter_by(season=season)

            # Take a shuffled list of available users which do not have a meet in the current season
            potential = []

            available_users = [usr for usr in users if usr.id != cur_user.id]
            for a_usr in available_users:
                take = True
                for meet in meets:
                    if a_usr.id == meet.uid1 or a_usr.id == meet.uid2:
                        take = False
                        break
                if take:
                    potential.append(a_usr)
            random.shuffle(potential)


            if len(potential) > 0:
                pair = potential[0]

                if self.__check_exist(season.get("previous"), {"uid1": cur_user.id, "uid2": pair.id}):
                    for_rand_distr.append(uid)
                else:
                    # TODO
                    self.add(cur_user, pair, season)
                    users.remove(pair)
            else:
                # TODO
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

    def add(self, meet: Meet) -> Meet:
        with self.session_factory() as session:
            session.add(meet)
            session.commit()
            session.refresh(meet)
            return meet

    def delete_by_id(self, id: str) -> None:
        with self.session_factory() as session:
            entity: Meet = session.query(Meet).filter_by(uid1=id).first()
            if not entity:
                raise MeetNotFoundError(id)
            session.delete(entity)

            # nope, delete!
            session.query(Meet).filter_by(uid2=id).update(dict(
                uid2="deleted"
            ))

            session.commit()

    def list(self, spec: Mapping = None) -> Iterator[Meet]:
        with self.session_factory() as session:
            objs = session.query(Meet).all()

        return filter.filtration(spec, objs)
