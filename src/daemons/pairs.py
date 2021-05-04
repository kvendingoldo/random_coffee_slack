# -*- coding: utf-8 -*-

import time
import datetime
from random import randrange, shuffle

from database.interface import connector


def create(sclient, usersDAO, period=60):
    # users = []
    #
    # season = datetime.datetime.now().strftime("%Y%V")
    #
    # for user in users:
    #     sql_statement = f"SELECT AVAIL.user" \
    #                     f"FROM (SELECT uid2 AS user FROM rating where uid1 = ? ORDER BY value DESC) AVAIL" \
    #                     f"LEFT JOIN (" \
    #                     f"SELECT DISTINCT user" \
    #                     f"FROM (" \
    #                     f"SELECT uid2 AS user, season" \
    #                     f"FROM meets" \
    #                     f"WHERE uid1 = ?" \
    #                     f"UNION" \
    #                     f"SELECT uid1 AS user, season" \
    #                     f"FROM meets" \
    #                     f"WHERE uid2 = ?" \
    #                     f") RES" \
    #                     f"WHERE season = ?" \
    #                     f") BUSY ON AVAIL.user = BUSY.user" \
    #                     f"WHERE BUSY.user IS null;"
    #     user2 = ""
    #     # get result
    #
    #     meetDao.add(user1, user2, season)

    ready = usersDAO.ready_all()
    if len(ready) % 2 == 0:
        ready.pop(randrange(0, len(ready)))
        shuffle(ready)
        pairs = zip(ready[::2], ready[1::2])

    # TODO: kvendingoldo after implementation of DAO layer
    while True:
        # make pairs
        # notify user
        print("pairs daemons")

        sclient.chat_postMessage(channel="U01THB38EDV",
                                 text="Hey!👋\n\n" \
                                      "This week your Random Coffee partner is @nickname!\n\n" \
                                      "Lucky you :)\n\n" \
                                      "Slack them now to set up a meeting."
                                 )
        time.sleep(period)
