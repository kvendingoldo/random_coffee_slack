# -*- coding: utf-8 -*-

import time

from database.dao import users
from database.interface import connector
from datetime import date


def meet_reminder(sclient, user):
    # TODO: check if meeting hasn't been done
    completed = False

    if not completed:
        # TODO: get partner name
        sclient.chat_postMessage(channel=user.uid,
                                 text="Привет!\n"
                                      "✉️ Уже середина недели,\n"
                                      "Напиши своему партнеру @username по Random Coffee, если вдруг забыл(а)."
                                 )


def ask_about_meet(sclient, user):
    sclient.chat_postMessage(channel=user.uid,
                             text="",
                             blocks=[
                                 {
                                     "type": "section",
                                     "text": {

                                         "type": "mrkdwn",
                                         "text": "Завершилась неделя встреч Random Coffee.\n"
                                                 "Небольшой опрос. \n"
                                                 "Состоялась встреча c @kvendingoldo?",
                                     },

                                 },
                                 {
                                     "type": "actions",
                                     "elements": [
                                         {
                                             "type": "button",
                                             "text": {
                                                 "type": "plain_text",
                                                 "emoji": True,
                                                 "text": "Yes"
                                             },
                                             "style": "primary",
                                             "action_id": "flow_meet_was"
                                         },
                                         {
                                             "type": "button",
                                             "text": {
                                                 "type": "plain_text",
                                                 "emoji": True,
                                                 "text": "No"
                                             },
                                             "style": "danger",
                                             "action_id": "flow_meet_was_not"
                                         }
                                     ]
                                 }
                             ]
                             )
    # TODO: do smth with rating


def ask_about_next_week(sclient, user):
    sclient.chat_postMessage(channel=user.uid,
                             text="",
                             blocks=[
                                 {
                                     "type": "section",
                                     "text": {

                                         "type": "mrkdwn",
                                         "text": "Привет!\n"
                                                 "Встречи Random Coffee продолжаются\n"
                                                 "Участвуешь на следующей неделе? \n"
                                                 "Будут вопросы, пиши в чат `help`",
                                     },

                                 },
                                 {
                                     "type": "actions",
                                     "elements": [
                                         {
                                             "type": "button",
                                             "text": {
                                                 "type": "plain_text",
                                                 "emoji": True,
                                                 "text": "Yes"
                                             },
                                             "style": "primary",
                                             "action_id": "flow_next_week_yes"
                                         },
                                         {
                                             "type": "button",
                                             "text": {
                                                 "type": "plain_text",
                                                 "emoji": True,
                                                 "text": "No"
                                             },
                                             "style": "danger",
                                             "action_id": "flow_next_week_no"
                                         }
                                     ]
                                 }
                             ]
                             )


def care(slack_client, connection_pool, period):
    connector = connector.Connector(connection_pool)

    while True:
        for user in users.list(connector):
            cur_day = date.today().weekday()

            if cur_day == 2:
                meet_reminder(slack_client, user)

            if cur_day == 4:
                ask_about_next_week(slack_client, user)
                ask_about_meet(slack_client, user)

        time.sleep(period)
