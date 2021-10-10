# -*- coding: utf-8 -*-

from sqlalchemy import Column, Boolean, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func

from db.database import Base
from constants import common


class Notification(Base):
    __tablename__ = common.DB_TABLES.notification

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    uid = Column(String(48), ForeignKey(f"{common.DB_TABLES.user}.id", ondelete="CASCADE"), unique=False, nullable=False)
    season = Column(String(24), unique=False, nullable=False)
    type = Column(String(24), unique=False, nullable=False)
    status = Column(Boolean, unique=False, nullable=False, default=False)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<Notification(id="{self.id}", ' \
               f'uid="{self.uid}", ' \
               f'season="{self.season}", ' \
               f'type="{self.type}", ' \
               f'status="{self.status}")>'
