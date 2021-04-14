# -*- coding: utf-8 -*-

from yoyo import read_migrations
from yoyo import get_backend


# TODO
def migrate():
    backend = get_backend('mysql://myuser@localhost/mydatabase')
    migrations = read_migrations('path/to/migrations')

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
