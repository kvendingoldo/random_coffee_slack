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

    def get_by_uid(self, uid: str) -> Notification:
        with self.session_factory() as session:
            notification = session.query(Notification).filter(Notification.uid == uid).first()
            if not notification:
                raise NotificationNotFoundError(id)
            return notification

    def update(self, notification: Notification) -> None:
        with self.session_factory() as session:
            session.query(Notification).filter_by(id=notification.id).update(dict(
                info=notification.info,
                reminder=notification.reminder,
                feedback=notification.feedback,
                next_week=notification.next_week
            ))

            session.commit()
