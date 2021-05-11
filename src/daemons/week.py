# -*- coding: utf-8 -*-

import time
import datetime

from database.dao import users as users_dao
from database.dao import meets as meets_dao
from database.interface import connector as db

from utils import season


def meet_info(client, meetsDao, user):
    season_id = season.get_current()
    uid = meetsDao.get_partner_uid(season_id, user.uid)

    client.chat_postMessage(channel=user.uid,
                            text=f"Hey!👋 \n\n" \
                                 f"This week your Random Coffee partner is <@{uid}>! Lucky you :) \n\n" \
                                 f"Slack them now to set up a meeting."
                            )


def meet_reminder(client, user):
    # TODO: check if meeting hasn't been done
    completed = False

    if not completed:
        client.chat_postMessage(channel=user.uid,
                                text="✉️ How are things?\n\n" \
                                     "Meed-week is the best day to set up a meeting with your coffee partner!\n\n" \
                                     "Slack them now to set up a meeting."
                                )


def meet_feedback(client, meetsDao, user):
    season_id = season.get_current()
    uid = meetsDao.get_partner_uid(season_id, user.uid)

    client.chat_postMessage(channel=user.uid,
                            text="",
                            blocks=[
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "The week is over! \n\n" \
                                                f"Did you get a chance to catch up with <@{uid}> for a coffee break?"
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
                                         "text": "New week – new opportunities!\n\n" \
                                                 "Are you taking part in Random Coffee meetings next week?"

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
                                                 "text": "Sure!"
                                             },
                                             "style": "primary",
                                             "action_id": "flow_next_week_yes"
                                         },
                                         {
                                             "type": "button",
                                             "text": {
                                                 "type": "plain_text",
                                                 "emoji": True,
                                                 "text": "One-week pause"
                                             },
                                             "style": "danger",
                                             "action_id": "flow_next_week_pause_1w"
                                         },
                                         {
                                             "type": "button",
                                             "text": {
                                                 "type": "plain_text",
                                                 "emoji": True,
                                                 "text": "One-month pause"
                                             },
                                             "style": "danger",
                                             "action_id": "flow_next_week_pause_1m"
                                         },
                                         {
                                             "type": "button",
                                             "text": {
                                                 "type": "plain_text",
                                                 "emoji": True,
                                                 "text": "Stop bot permanently"
                                             },
                                             "style": "danger",
                                             "action_id": "flow_stop"
                                         }
                                     ]
                                 }
                             ]
                             )


def care(client, connection_pool, config):
    connector = db.Connector(connection_pool)
    # weekday = date.today().weekday() + 1
    weekday = 5

    usersDao = users_dao.UsersDAO(connector)
    meetsDao = meets_dao.MeetsDao(connector)

    users = usersDao.list()

    while True:
        for user in users:
            if weekday == 1:
                meet_info(client, meetsDao, user)
            elif weekday == 3:
                meet_reminder(client, user)
            elif weekday == 5:
                meet_feedback(client, meetsDao, user)
            elif weekday == 7:
                ask_about_next_week(client, user)

        time.sleep(config["daemons"]["week"]["poolPeriod"])
