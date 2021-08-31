# -*- coding: utf-8 -*-

import time

from loguru import logger

from datetime import date
from database import exceptions
from utils import season
from constants import messages


def meet_info(client, meetDao, user):
    try:
        uid = meetDao.get_uid2_by_id(
            season.get(), user.uid
        )

        client.chat_postMessage(
            channel=user.uid,
            text=messages.MEET_INFO.format(uid)
        )
    except:
        logger.error("Info message didn't send")

    else:
        logger.info("Info message sent")


def meet_reminder(client, meetDao, user):
    completed = meetDao.get_status_by_id(season.get(), user.uid)

    if not completed:
        client.chat_postMessage(
            channel=user.uid,
            text="",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": messages.MEET_REMINDER
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
        uid = meetsDao.get_uid2_by_id(season.get(), user.uid)

        client.chat_postMessage(
            channel=user.uid,
            text="",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": messages.MEET_FEEDBACK.format(uid)

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
                    "text": messages.MEET_NEXT

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
        weekday = date.today().weekday() + 1
        users = userDAO.list()
        user_avail_ids = userDAO.list_ids(only_available=True)

        if weekday == 1:
            if len(user_avail_ids) > 1:
                meetDAO.create(user_avail_ids, config)
        for user in users:
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
