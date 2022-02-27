# -*- coding: utf-8 -*-

from pydantic.dataclasses import dataclass


@dataclass
class NotificationTypes:
    info: str = 'info'
    looking: str = 'looking'
    reminder: str = 'reminder'
    feedback: str = 'feedback'
    next_week: str = 'next_week'


@dataclass
class DBTables:
    user: str = 'user'
    meet: str = 'meet'
    meta: str = 'meta'
    rating: str = 'rating'
    notification: str = 'notification'


NTF_TYPES = NotificationTypes()
DB_TABLES = DBTables()
