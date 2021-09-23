# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer

from database.database import Base
from constants import tables


class User(Base):
    __tablename__ = tables.USERS

    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String, unique=False)
    pause_in_weeks = Column(String, unique=False, default="0")
    loc = Column(String, unique=False, default="none")

    def __repr__(self):
        return f'<User(id="{self.id}", ' \
               f'username="{self.username}", ' \
               f'uid="{self.uid}", ' \
               f'pause_in_weeks="{self.pause_in_weeks}", ' \
               f'loc="{self.loc}")>'

    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.id and self.uid == other.uid and self.username == other.username \
                   and self.pause_in_weeks == other.pause_in_weeks and self.loc == other.loc
        return False
