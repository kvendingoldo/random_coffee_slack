# -*- coding: utf-8 -*-

import time

from datetime import date
from loguru import logger
from utils import season, repo
from constants import messages, elements
from models.notification import Notification
from db.exceptions import NotificationNotFoundError


def meet_msg(client, ntf_repo, pair, msg_type, msg_text, msg_blocks=None, inline_msg_block=False):
    if msg_blocks is None:
        msg_blocks = []

    try:
        ntf = ntf_repo.list({"id": pair["id"]})[0]
        if getattr(ntf, msg_type):
            logger.info(f"Users {pair['uid1']}, {pair['uid2']} has already notified about {msg_type}")
        else:
            if inline_msg_block:
                client.chat_postMessage(
                    channel=pair['uid1'],
                    blocks=[{
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": msg_text.format(pair['uid2'])
                        },

                    }] + msg_blocks
                )
            else:
                client.chat_postMessage(
                    channel=pair['uid1'], text=msg_text.format(pair['uid2']), blocks=msg_blocks
                )

            logger.info(f"{msg_type} message sent for {pair['uid1']} (pair: {pair['uid2']})")

            setattr(ntf, msg_type, True)
            ntf_repo.update(ntf)

    except Exception as ex:
        logger.error(f"{msg_type} message didn't send for user #{pair['uid1']}, error: {ex}")


def care(client, user_repo, meet_repo, ntf_repo, config):
    while True:
        season_id = season.get()
        weekday = 5
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

        meets = meet_repo.list(spec={"season": season_id})
        pairs = []

        # NOTE: Create pairs (it's the same as meets, but more convenient form
        for meet in meets:
            pairs.append({"uid1": meet.uid1, "uid2": meet.uid2, "meet_id": meet.id,
                          "id": repo.calc_ntf_hash(meet.uid1, meet.uid2, meet.id)})
            pairs.append({"uid1": meet.uid2, "uid2": meet.uid1, "meet_id": meet.id,
                          "id": repo.calc_ntf_hash(meet.uid2, meet.uid1, meet.id)})

        # NOTE: notify users
        for pair in pairs:
            if weekday <= 5:
                try:
                    ntf = ntf_repo.list({"id": pair["id"]})
                    if not ntf:
                        ntf_repo.add(Notification(id=pair['id'], meet_id=pair['meet_id']))
                        logger.info(f"Notification for meet {pair['meet_id']} has created")
                except NotificationNotFoundError:
                    ntf_repo.add(Notification(id=pair['id'], meet_id=pair['meet_id']))
                    logger.info(f"Notification for meet {pair['meet_id']} has created")

                meet_msg(client, ntf_repo, pair, "info", messages.MEET_INFO)
                meet_msg(
                    client, ntf_repo, pair, "reminder", messages.MEET_REMINDER, elements.MEET_REMINDER, True
                )
            elif weekday == 6:
                meet_msg(
                    client, ntf_repo, pair, "feedback", messages.MEET_FEEDBACK, elements.MEET_FEEDBACK,
                    True
                )
            elif weekday == 7:
                meet_msg(
                    client, ntf_repo, pair, "next_week", messages.MEET_NEXT, elements.MEET_NEXT, True
                )

        # NOTE: Change pause_in_weeks for all users
        # NOTE: nullify notifications for all users
        if weekday == 7:
            for usr in user_repo.list():
                if int(usr.pause_in_weeks) > 0:
                    usr.pause_in_weeks = str(int(usr.pause_in_weeks) - 1)
                    user_repo.update(usr)

            for ntf in ntf_repo.list():
                ntf_repo.nullify(ntf)

        time.sleep(config["daemons"]["week"]["poolPeriod"])
