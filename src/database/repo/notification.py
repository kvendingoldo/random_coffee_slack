# -*- coding: utf-8 -*-

from contextlib import AbstractContextManager
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from models.notification import Notification
from database.exceptions import NotificationNotFoundError

COLUMNS = ["info", "reminder", "feedback", "next_week"]


class NotificationRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def is_notified(self, uid: str, column: str) -> bool:
        if column not in COLUMNS:
            raise ValueError(f"Wrong value for notification column name: {column}")

        with self.session_factory() as session:
            notification = session.query(Notification).filter(Notification.uid == uid).first()
            if not notification:
                raise NotificationNotFoundError(uid)
            return bool(getattr(notification, column))

    def update(self, user: User) -> None:
        # todo
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

    def change_all(self, uid, notified="1"):
        for column in COLUMNS:
            self.change_column(uid, column, notified)
