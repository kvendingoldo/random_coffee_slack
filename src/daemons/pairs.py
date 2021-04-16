# -*- coding: utf-8 -*-

import time
from random import randrange, shuffle

from database.interface import connector


def create(sclient, usersDAO, period=60):
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
                                 text="Привет!\n"
                                      "Твоя пара в random coffee на эту неделю: @nickname \n"
                                      "Не откладывай, договорись о встрече сразу 🙂 \n"
                                      "Будут вопросы, пиши в чат `help`.\n"
                                      "👨‍💻 Рекомендуем на этой неделе провести встречу по видеосвязи.\n"
                                      "Берегите себя и близких! И поддерживайте общение с окружающими онлайн")
        time.sleep(period)
