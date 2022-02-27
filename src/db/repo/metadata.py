# -*- coding: utf-8 -*-

from contextlib import AbstractContextManager
from typing import Callable, Iterator, Mapping

from sqlalchemy.orm import Session

from utils import repo
from models.metadata import Metadata
from db.exceptions import MetadataNotFoundError


class MetadataRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get(self, spec: Mapping = None) -> Metadata:
        objs = self.list(spec)

        if not objs:
            raise MetadataNotFoundError("")
        else:
            return objs[0]

    def add(self, metadata: Metadata) -> Metadata:
        with self.session_factory() as session:
            session.add(metadata)
            session.commit()
            session.refresh(metadata)
            return metadata

    def update(self, metadata: Metadata) -> None:
        with self.session_factory() as session:
            try:
                session.query(Metadata).filter_by(id=metadata.id).update(dict(
                    name=metadata.name,
                    value=metadata.value,
                ))
                session.commit()
            except Exception as ex:
                # TODO: add warn log
                session.add(metadata)
                session.commit()
                session.refresh(metadata)

    def list(self, spec: Mapping = None) -> Iterator[Metadata]:
        with self.session_factory() as session:
            objs = session.query(Metadata).all()
            if not objs:
                return []
        return repo.filtration(spec, objs)
