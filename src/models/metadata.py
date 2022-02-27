# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func

from db.database import Base
from constants import common


class Metadata(Base):
    __tablename__ = common.DB_TABLES.meta

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = Column(String(48), unique=False, nullable=False)
    value = Column(String(92), unique=False, nullable=False)

    tmst_created = Column(DateTime(timezone=True), server_default=func.now())
    tmst_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<Metadata(id="{self.id}", ' \
               f'name="{self.name}", ' \
               f'value="{self.value}")>'
