# -*- coding: utf-8 -*-

from contextlib import contextmanager, AbstractContextManager
from typing import Callable
from loguru import logger

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(
            db_url,
            echo=False,
            echo_pool=False,
            logging_name="sqlalchemy.engine",
            pool_logging_name="sqlalchemy.pool",
            max_overflow=1,
            pool_pre_ping=True,
            pool_size=5,
            pool_recycle=1800
        )
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception('Session rollback because of exception')
            session.rollback()
            raise
        finally:
            session.close()
