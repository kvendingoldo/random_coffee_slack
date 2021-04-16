# -*- coding: utf-8 -*-

import time
from database.interface import connector


def create(sclient, connection_pool, period=60):
    connector = connector.Connector(connection_pool)

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
