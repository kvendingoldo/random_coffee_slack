# -*- coding: utf-8 -*-

from sqlalchemy import Column, Boolean, String, Integer

from db.database import Base
from constants import tables


class Notification(Base):
    __tablename__ = tables.NOTIFICATIONS

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    uid = Column(String, primary_key=True, unique=True)
    info = Column(Boolean, unique=False, default=False)
    reminder = Column(Boolean, unique=False, default=False)
    feedback = Column(Boolean, unique=False, default=False)
    next_week = Column(Boolean, unique=False, default=False)

    def __repr__(self):
        return f'<Notification(id="{self.id}", ' \
               f'uid="{self.uid}", ' \
               f'info="{self.info}", ' \
               f'reminder="{self.reminder}", ' \
               f'feedback="{self.feedback}", ' \
               f'next_week="{self.next_week}")>'
