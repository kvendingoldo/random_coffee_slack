# -*- coding: utf-8 -*-

from contextlib import AbstractContextManager
from typing import Callable, Iterator, Mapping

from sqlalchemy.orm import Session

from utils import repo
from models.notification import Notification
from db.exceptions import NotificationNotFoundError


class NotificationRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get(self, spec: Mapping = None) -> Notification:
        objs = self.list(spec)

        if not objs:
            raise NotificationNotFoundError("")
        else:
            return objs[0]

    def add(self, notification: Notification) -> Notification:
        with self.session_factory() as session:
            session.add(notification)
            session.commit()
            session.refresh(notification)
            return notification

    def update(self, notification: Notification) -> None:
        with self.session_factory() as session:
            try:
                session.query(Notification).filter_by(id=notification.id).update(dict(
                    uid=notification.uid,
                    season=notification.season,
                    type=notification.type,
                    status=notification.status
                ))
                session.commit()
            except Exception as ex:
                # TODO: add warn log
                session.add(notification)
                session.commit()
                session.refresh(notification)

    def list(self, spec: Mapping = None) -> Iterator[Notification]:
        with self.session_factory() as session:
            objs = session.query(Notification).all()
            if not objs:
                return []
        return repo.filtration(spec, objs)
