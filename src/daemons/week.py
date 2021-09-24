# -*- coding: utf-8 -*-

import time

from loguru import logger

from datetime import date
from utils import season
from constants import messages

from models.meet import Meet

from models.notification import Notification
from db.exceptions import NotificationNotFoundError


def meet_info(client, user, meets, notification_repo):
    if len(meets) > 0:
        try:
            if notification_repo.is_notified(user.id, "info"):
                logger.info(f"User {user.id} has already notified about meet")
            else:
                for idx, meet in enumerate(meets):
                    uid = meet.uid2 if meet.uid1 == user.id else meet.uid1

                    if idx == 0:
                        msg = messages.MEET_INFO.format(uid)
                    else:
                        msg = messages.MEET_INFO_ADDITIONAL.format(uid)

                    client.chat_postMessage(channel=user.id, text=msg)

                    logger.info(f"Info message sent for {user.id} (meet with {uid})")

                try:
                    notification = notification_repo.get_by_uid(user.id)
                    notification.info = True
                    notification_repo.update(notification)
                except NotificationNotFoundError:
                    notification = Notification()
                    notification.uid = user.id
                    notification.info = True
                    notification_repo.add(notification)


        except Exception as ex:
            logger.error(f"Info message didn't send for {user.id}, error: {ex}")
    else:
        logger.info(f"User {user.id} does not have any meets")


def meet_reminder(client, meetDao, notificationDao, user):
    completed = meet_repo.get_by_spec(
        uid1=user.uid,
        season=season.get()
    ).status

    completed = meetDao.get_status_by_id(season.get(), user.uid)

    if not completed:
        if notificationDao.is_notified(user.uid, "reminder"):
            logger.info(f"{user.uid} has been notified of reminder")
        else:
            notification = notification_repo.get_by_uid(user.uid)
            notification.reminder = "1"
            notification_repo.update(notification)

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


def meet_feedback(client, meetsDao, notificationDao, user):
    if notificationDao.is_notified(user.uid, "feedback"):
        logger.info(f"{user.uid} has already notified about feedback")
    else:
        notification = notification_repo.get_by_uid(user.uid)
        notification.feedback = "1"
        notification_repo.update(notification)

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


def ask_about_next_week(sclient, notificationDao, user):
    if notificationDao.is_notified(user.uid, "next_week"):
        logger.info(f"{user.uid} has already notified about next week")
    else:
        notification = notification_repo.get_by_uid(user.uid)
        notification.next_week = "1"
        notification_repo.update(notification)

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
                            "action_id": "stop"
                        }
                    ]
                }
            ]
        )


def care(client, user_repo, meet_repo, notification_repo, config):
    while True:
        season_id = season.get()
        weekday = 4
        # date.today().weekday() + 1
        users = user_repo.list(spec={"pause_in_weeks": "0"})

        logger.info(f"Care about the current week. Today is {weekday} day of week ...")

        if weekday < 5:
            meet_repo.create(
                [user.id for user in users]
            )
        elif weekday == 5:
            meet_repo.create(
                users=[user.id for user in users],
                additional_users=config["bot"]["additionalUsers"]
            )
        for user in users:
            if weekday <= 5:
                meets = meet_repo.list(spec={"season": season_id, "uid1": user.id}) + \
                        meet_repo.list(spec={"season": season_id, "uid2": user.id})

                meet_info(client, user, meets, notification_repo)
                # meet_reminder(client, meetDAO, notificationDao, user)
            elif weekday == 6:
                pass
                # meet_feedback(client, meetDAO, notificationDao, user)
            elif weekday == 7:
                notification_repo.update(
                    Notification(
                        uid=user.uid, info="0", reminder="0", feedback="0", next_week="0"
                    )
                )

                # ask_about_next_week(client, notification_repo, user)

                # for u in user_repo.list():
                #     u.pause_in_weeks = str(int(u.pause_in_weeks) - 1)
                #     user_repo.update(u)

        time.sleep(config["daemons"]["week"]["poolPeriod"])
