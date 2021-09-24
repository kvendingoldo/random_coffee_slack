# -*- coding: utf-8 -*-

import time

from loguru import logger

from datetime import date
from utils import season
from constants import messages, elements
from models.notification import Notification


def meet_msg(client, meet, notification_repo, type, msg_text, msg_blocks=None, inline_msg_block=False):
    if msg_blocks is None:
        msg_blocks = []

    try:
        ntf = notification_repo.list({"meet_id": meet.id})[0]

        if getattr(ntf, type):
            logger.info(f"Users {meet.uid1}, {meet.uid2} has already notified about {type}")
        else:
            if inline_msg_block:
                client.chat_postMessage(
                    channel=meet.uid1,
                    blocks=[{
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": msg_text.format(meet.uid2)
                        },

                    }] + msg_blocks
                )
                logger.info(f"{type} message sent for {meet.uid1} (pair: {meet.uid2})")

                client.chat_postMessage(
                    channel=meet.uid2,
                    blocks=[{
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": msg_text.format(meet.uid1)
                        },

                    }] + msg_blocks
                )
                logger.info(f"{type} message sent for {meet.uid2} (pair: {meet.uid1})")
            else:
                client.chat_postMessage(
                    channel=meet.uid1, text=msg_text.format(meet.uid2), blocks=msg_blocks
                )
                logger.info(f"{type} message sent for {meet.uid1} (pair: {meet.uid2})")

                client.chat_postMessage(
                    channel=meet.uid2, text=msg_text.format(meet.uid1), blocks=msg_blocks
                )
                logger.info(f"{type} message sent for {meet.uid2} (pair: {meet.uid1})")

            setattr(ntf, type, True)
            notification_repo.update(ntf)
    except Exception as ex:
        logger.error(f"{type} message didn't send for meet #{meet.id}, error: {ex}")


def care(client, user_repo, meet_repo, notification_repo, config):
    while True:
        season_id = season.get()
        weekday = 7
        # date.today().weekday() + 1
        users = user_repo.list(spec={"pause_in_weeks": "0"})

        logger.info(f"Care about the current week. Today is {weekday} day of week ...")

        # NOTE: create meets
        if weekday < 5:
            meet_repo.create(
                uids=[user.id for user in users]
            )
        elif weekday == 5:
            meet_repo.create(
                uids=[user.id for user in users],
                additional_uids=config["bot"]["additionalUsers"]
            )

        # NOTE: create notifications
        if weekday <= 5:
            ntf_meet_ids = [ntf.meet_id for ntf in notification_repo.list()]

            for meet in meet_repo.list(spec={"season": season_id}):
                if meet.id in ntf_meet_ids:
                    logger.info(f"Notification for meet {meet.id} is already exist")
                else:
                    ntf = Notification()
                    ntf.meet_id = meet.id

                    notification_repo.add(ntf)
                    logger.info(f"Notification for meet {meet.id} has created")

        # NOTE: notify users
        for meet in meet_repo.list(spec={"season": season_id}):
            if weekday <= 5:
                meet_msg(client, meet, notification_repo, "info", messages.MEET_INFO)
                meet_msg(client, meet, notification_repo, "reminder", "", elements.MEET_REMINDER)
            elif weekday == 6:
                meet_msg(
                    client, meet, notification_repo, "feedback", messages.MEET_FEEDBACK, elements.MEET_FEEDBACK, True
                )
            elif weekday == 7:
                meet_msg(
                    client, meet, notification_repo, "next_week", messages.MEET_NEXT, elements.MEET_NEXT, True
                )

        # NOTE: Change pause_in_weeks for all users
        if weekday == 7:
            for usr in user_repo.list():
                if int(usr.pause_in_weeks) > 0:
                    usr.pause_in_weeks = str(int(usr.pause_in_weeks) - 1)
                    user_repo.update(usr)

        time.sleep(config["daemons"]["week"]["poolPeriod"])
