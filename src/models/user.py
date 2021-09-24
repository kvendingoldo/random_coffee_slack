# -*- coding: utf-8 -*-

from sqlalchemy import Column, String

from db.database import Base
from constants import tables


class User(Base):
    __tablename__ = tables.USERS

    id = Column(String(48), primary_key=True, nullable=False, unique=True)
    username = Column(String(92), nullable=False, unique=False)
    pause_in_weeks = Column(String(10), nullable=False, unique=False, default="0")
    loc = Column(String(24), nullable=False, unique=False, default="none")

    def __repr__(self):
        return f'<User(id="{self.id}", ' \
               f'username="{self.username}", ' \
               f'pause_in_weeks="{self.pause_in_weeks}", ' \
               f'loc="{self.loc}")>'
