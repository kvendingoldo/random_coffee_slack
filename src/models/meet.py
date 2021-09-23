# -*- coding: utf-8 -*-

from sqlalchemy import Column, Boolean, Integer, String

from database.database import Base
from constants import tables


class Meet(Base):
    __tablename__ = tables.MEETS

    id = Column(Integer, primary_key=True, unique=True)
    season = Column(String, unique=False)
    uid1 = Column(String, unique=False)
    uid2 = Column(String, unique=False)
    completed = Column(Boolean, unique=False, default=False)

    def __repr__(self):
        return f'<Meet(id="{self.id}", ' \
               f'season="{self.season}", ' \
               f'uid1="{self.uid1}", ' \
               f'uid2="{self.uid2}", ' \
               f'completed="{self.completed}")>'
