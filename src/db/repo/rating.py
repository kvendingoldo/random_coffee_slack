# -*- coding: utf-8 -*-

from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from models.rating import Rating
from models.user import User
from db.exceptions import RatingNotFoundError


class RatingRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def add(self, id: str) -> None:
        with self.session_factory() as session:
            users: User = session.query(User).filter(User.id != id)

            for user in users:
                session.add(
                    Rating(uid1=user.id, uid2=id, value=1.0)
                )
                session.add(
                    Rating(uid1=id, uid2=user.id, value=1.0)
                )
            session.commit()

            return None

    def get_by_ids(self, uid1: str, uid2: str) -> Rating:
        with self.session_factory() as session:
            user = session.query(Rating).filter(
                and_(Rating.uid1 == uid1, Rating.uid2 == uid2)
            ).first()
            if not user:
                raise RatingNotFoundError(id)
            return user

    def delete_by_id(self, id: str) -> None:
        with self.session_factory() as session:
            entity: Rating = session.query(Rating).filter(
                or_(Rating.uid1 == id, Rating.uid2 == id)
            ).first()
            if not entity:
                raise RatingNotFoundError(id)
            session.delete(entity)
            session.commit()

    def update(self, rating: Rating) -> None:
        with self.session_factory() as session:
            session.query(Rating).filter(
                and_(Rating.uid1 == rating.uid1, Rating.uid2 == rating.uid2)
            ).update(dict(
                value=rating.value,
            ))

            session.commit()
