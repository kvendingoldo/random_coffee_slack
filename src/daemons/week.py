# -*- coding: utf-8 -*-

import time

from database import exceptions
from utils import season


def meet_info(client, meetDao, user):
    uid = meetDao.get_partner_uid(
        season.get_current(), user.uid
    )

    client.chat_postMessage(
        channel=user.uid,
        text="Hey!👋 \n\n"
             f"This week your Random Coffee partner is <@{uid}>! Lucky you :) \n\n"
             "Slack them now to set up a meeting."
    )


def meet_reminder(client, meetDao, user):
    completed = meetDao.get_status(season.get_current(), user.uid)

    if not completed:
        client.chat_postMessage(
            channel=user.uid,
            text="",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "✉️ How are things?\n\n" \
                                "Meed-week is the best day to set up a meeting with your coffee partner!\n\n" \
                                "Slack them now to set up a meeting."
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
                                "text": "We've already had a meeting"
                            },
                            "style": "primary",
                            "action_id": "flow_meet_had"
                        }
                    ]
                }
            ]
        )


def meet_feedback(client, meetsDao, user):
    try:
        uid = meetsDao.get_partner_uid(
            season.get_current(), user.uid
        )

        client.chat_postMessage(
            channel=user.uid,
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
    except exceptions.NoResultFound:
        pass


def ask_about_next_week(sclient, user):
    sclient.chat_postMessage(
        channel=user.uid,
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


def care(client, userDAO, meetDAO, config):
    while True:
        # weekday = date.today().weekday() + 1
        weekday = 1
        users = userDAO.list()
        user_avail_ids = userDAO.list_ids(only_available=True)

        if weekday == 1:
            #pass
            meetDAO.create(user_avail_ids)

        for user in users:
            if user.uid != "U01THB38EDV2" and user.uid != "U01THB38EDV1":
                if weekday == 1:

                    meet_info(client, meetDAO, user)
                elif weekday == 3:
                    meet_reminder(client, meetDAO, user)
                elif weekday == 5:
                    meet_feedback(client, meetDAO, user)
                elif weekday == 7:
                    ask_about_next_week(client, user)
                    userDAO.decrement_users_pause(1)

        time.sleep(config["daemons"]["week"]["poolPeriod"])
