# -*- coding: utf-8 -*-

from sqlalchemy import Column, Boolean, Integer, ForeignKey, String

from db.database import Base
from constants import tables


class Notification(Base):
    __tablename__ = tables.NOTIFICATIONS

    id = Column(String(48), primary_key=True, nullable=False, unique=True)
    info = Column(Boolean, unique=False, nullable=False, default=False)
    reminder = Column(Boolean, unique=False, nullable=False, default=False)
    feedback = Column(Boolean, unique=False, nullable=False, default=False)
    next_week = Column(Boolean, unique=False, nullable=False, default=False)
    meet_id = Column(Integer, ForeignKey(f"{tables.MEETS}.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f'<Notification(id="{self.id}", ' \
               f'info="{self.info}", ' \
               f'reminder="{self.reminder}", ' \
               f'feedback="{self.feedback}", ' \
               f'next_week="{self.next_week}", ' \
               f'meet_id="{self.meet_id}")>'
