"""Repositories module."""

from contextlib import AbstractContextManager
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from models.user import User


class UserRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def add(self, user: User) -> User:
        with self.session_factory() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def delete_by_id(self, id: str) -> None:
        with self.session_factory() as session:
            entity: User = session.query(User).filter(User.id == id).first()
            if not entity:
                raise UserNotFoundError(id)
            session.delete(entity)
            session.commit()

    def update(self, user: User) -> None:
        with self.session_factory() as session:
            entity: User = session.query(User).filter_by(id=user.id).first()
            if not entity:
                raise UserNotFoundError(user.id)

            session.query(User).filter_by(id=user.id).update(dict(
                username=user.username,
                pause_in_weeks=user.pause_in_weeks,
                loc=user.loc
            ))

            session.commit()

    def get_by_id(self, id: str) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == id).first()
            if not user:
                raise UserNotFoundError(id)
            return user

    def list(self) -> Iterator[User]:
        with self.session_factory() as session:
            return session.query(User).all()

    def list_ids(self, only_available: bool = False) -> Iterator[User]:
        with self.session_factory() as session:
            if only_available:
                users = session.query(User).filter(User.pause_in_weeks == "0").all()
            else:
                users = session.query(User).all()

            if users:
                raise Exception("")
            return users


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f'{self.entity_name} not found, id: {entity_id}')


class UserNotFoundError(NotFoundError):
    entity_name: str = 'User'
