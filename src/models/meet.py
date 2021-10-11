# -*- coding: utf-8 -*-

from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from db.database import Base
from constants import common


class Meet(Base):
    __tablename__ = common.DB_TABLES.meet

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    season = Column(String(24), unique=False, nullable=False)
    uid1 = Column(String(48), ForeignKey(f"{common.DB_TABLES.user}.id", ondelete="CASCADE"), unique=False, nullable=False)
    uid2 = Column(String(48), ForeignKey(f"{common.DB_TABLES.user}.id", ondelete="CASCADE"), unique=False, nullable=False)
    completed = Column(Boolean, unique=False, nullable=False, default=False)

    tmst_created = Column(DateTime(timezone=True), server_default=func.now())
    tmst_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<Meet(id="{self.id}", ' \
               f'season="{self.season}", ' \
               f'uid1="{self.uid1}", ' \
               f'uid2="{self.uid2}", ' \
               f'completed="{self.completed}")>'
