# -*- coding: utf-8 -*-

import time


def create(client, period=60):
    # TODO: kvendingoldo after implementation of DAO layer
    while True:
        # make pairs
        # notify user
        print("pairs algo")

        client.chat_postMessage(channel="D01TRBDB8EA",
                                text="Привет\\! Скучал? Я нашел для тебя [собеседника](tg://user?id=%s)\\. Скорее договаривайся о встрече в zoom/skype/баре или кофешопе\\! Надеюсь все пройдет успешно\\! Увидимся на следующей неделе")

        time.sleep(period)
