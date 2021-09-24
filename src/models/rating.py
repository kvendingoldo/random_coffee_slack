# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Float

from database.database import Base
from constants import tables


class Rating(Base):
    __tablename__ = tables.RATING

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    uid1 = Column(String, unique=False)
    uid2 = Column(String, unique=False)
    value = Column(Float, unique=False)

    def __repr__(self):
        return f'<Rating(id="{self.id}", ' \
               f'uid1="{self.uid1}", ' \
               f'uid2="{self.uid2}", ' \
               f'value="{self.value}")>'
