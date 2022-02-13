# -*- coding: utf-8 -*-

from db import database
from db.repo.user import UserRepository
from db.repo.notification import NotificationRepository
from db.repo.rating import RatingRepository
from db.repo.meet import MeetRepository


def get_repos(config):
    db_url = "mysql://{}:{}@{}:{}/{}".format(
        config["database"]["username"], config["database"]["password"],
        config["database"]["host"], config["database"]["port"],
        config["database"]["db"]
    )

    db = database.Database(db_url)
    db.create_database()

    user_repo = UserRepository(session_factory=db.session)
    ntf_repo = NotificationRepository(session_factory=db.session)
    rating_repo = RatingRepository(session_factory=db.session)
    meet_repo = MeetRepository(session_factory=db.session)

    return user_repo, ntf_repo, rating_repo, meet_repo
