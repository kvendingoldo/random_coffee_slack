# -*- coding: utf-8 -*-

from database.dao import users


def meet_reminder(sclient):
    # check that meet completed

    sclient.chat_postMessage(channel="D01TRBDB8EA",
                             text="Привет!\n"
                                  "✉️ Уже середина недели,\n"
                                  "Напиши своему партнеру Random Coffee, если вдруг забыл(а)."
                             )


def ask_about_next_week(sclient):
    sclient.chat_postMessage(channel="D01TRBDB8EA",
                             text="Привет!\n"
                                  "Встречи Random Coffee продолжаются\n"
                                  "Участвуешь на следующей неделе? \n"
                                  "Будут вопросы, пиши в чат `help`"
                             )


def care(sclient, db_connection):
    users = []

    for user in users.get_users(db_connection)

        # The mid of week
        if True:
            meet_reminder(sclient)

        # Friday
        if True:
            ask_about_next_week(sclient)
