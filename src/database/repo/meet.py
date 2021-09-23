# -*- coding: utf-8 -*-

from contextlib import AbstractContextManager
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from models.meet import Meet
from database.exceptions import MeetNotFoundError


class MeetRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

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

            session.query(Meet).filter_by(uid2=id).update(dict(
                uid2="deleted"
            ))

            session.commit()

    def get_by_spec(self, season: str) -> Iterator[Meet]:
        with self.session_factory() as session:
            meets = session.query(Meet).filter(season=season)
            if not meets:
                raise MeetNotFoundError(id)
            return meets

