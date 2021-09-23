# -*- coding: utf-8 -*-

from sqlalchemy import Column, String

from database.database import Base
from constants import tables


class User(Base):
    __tablename__ = tables.USERS

    id = Column(String, primary_key=True, unique=True)
    username = Column(String, unique=False)
    pause_in_weeks = Column(String, unique=False, default="0")
    loc = Column(String, unique=False, default="none")

    def __repr__(self):
        return f'<User(id="{self.id}", ' \
               f'username="{self.username}", ' \
               f'uid="{self.uid}", ' \
               f'pause_in_weeks="{self.pause_in_weeks}", ' \
               f'loc="{self.loc}")>'
