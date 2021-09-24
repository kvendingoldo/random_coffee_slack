# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Float, ForeignKey

from db.database import Base
from constants import tables


class Rating(Base):
    __tablename__ = tables.RATING

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    uid1 = Column(String(48), ForeignKey(f"{tables.USERS}.id", ondelete="CASCADE"), unique=False, nullable=False)
    uid2 = Column(String(48), ForeignKey(f"{tables.USERS}.id", ondelete="CASCADE"), unique=False, nullable=False)
    value = Column(Float, unique=False, nullable=False, default=1.0)

    def __repr__(self):
        return f'<Rating(id="{self.id}", ' \
               f'uid1="{self.uid1}", ' \
               f'uid2="{self.uid2}", ' \
               f'value="{self.value}")>'
