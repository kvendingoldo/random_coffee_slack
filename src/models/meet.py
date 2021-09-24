# -*- coding: utf-8 -*-

from sqlalchemy import Column, Boolean, Integer, String, ForeignKey

from db.database import Base
from constants import tables


class Meet(Base):
    __tablename__ = tables.MEETS

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    season = Column(String(24), unique=False, nullable=False)
    uid1 = Column(String(48), ForeignKey(f"{tables.USERS}.id", ondelete="CASCADE"), unique=False, nullable=False)
    uid2 = Column(String(48), ForeignKey(f"{tables.USERS}.id", ondelete="CASCADE"), unique=False, nullable=False)
    completed = Column(Boolean, unique=False, nullable=False, default=False)

    def __repr__(self):
        return f'<Meet(id="{self.id}", ' \
               f'season="{self.season}", ' \
               f'uid1="{self.uid1}", ' \
               f'uid2="{self.uid2}", ' \
               f'completed="{self.completed}")>'
