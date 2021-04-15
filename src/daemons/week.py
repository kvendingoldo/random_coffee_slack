# -*- coding: utf-8 -*-

from database.dao import users
from datetime import date


def meet_reminder(sclient):
    # check that meet completed

    sclient.chat_postMessage(channel="D01TRBDB8EA",
                             text="Привет!\n"
                                  "✉️ Уже середина недели,\n"
                                  "Напиши своему партнеру Random Coffee, если вдруг забыл(а)."
                             )


def ask_about_this_week(sclient):
    sclient.chat_postMessage(channel="D01TRBDB8EA",
                             text="Завершилась неделя встреч Random Coffee.\n"
                                  "Небольшой опрос. \n"
                                  "Состоялась встреча c UserX?"
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

    for user in users.get_users(db_connection):
        cur_day = date.today().weekday()

        if cur_day == 2:
            meet_reminder(sclient)

        if cur_day == 4:
            ask_about_next_week(sclient)
            ask_about_this_week(sclient)
