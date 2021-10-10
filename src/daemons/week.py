# -*- coding: utf-8 -*-

import time

from datetime import date
from loguru import logger
from utils import season, repo
from constants import messages, elements, common
from models.notification import Notification
from db.exceptions import NotificationNotFoundError


def send_msg(client, pair, dry_run, msg_text, msg_blocks, inline_msg_block):
    uid1 = pair["uid1"]
    uid2 = pair["uid2"]

    if dry_run:
        logger.info("[DRY-RUN]:\n" + msg_text.format(uid2))
    else:
        if inline_msg_block:
            client.chat_postMessage(
                channel=uid1,
                blocks=[{
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": msg_text.format(uid2)
                    },

                }] + msg_blocks
            )
        else:
            client.chat_postMessage(
                channel=uid1, text=msg_text.format(uid2), blocks=msg_blocks
            )


def msg_wrapper(client, ntf_repo, pair, msg_type, msg_text, dry_run=True, msg_blocks=None, inline_msg_block=False):
    if msg_blocks is None:
        msg_blocks = []

    uid1 = pair["uid1"]
    uid2 = pair["uid2"]

    try:
        ntf = ntf_repo.get({"uid": uid1, "type": msg_type, "season": season.get()})
        if ntf.status:
            logger.info(f"Users {uid1}, {uid2} has already notified about {msg_type}")
        else:
            send_msg(client, pair, dry_run, msg_text, msg_blocks, inline_msg_block)
            ntf.status = True
            ntf_repo.update(ntf)
            logger.info(f"{msg_type} message sent for {uid1} (pair: {uid2})")
    except NotificationNotFoundError as ex:
        logger.error(ex)
        send_msg(client, pair, dry_run, msg_text, msg_blocks, inline_msg_block)
        logger.info(f"{msg_type} message sent for {uid1} (pair: {uid2})")
        ntf_repo.add(Notification(uid=uid1, season=season.get(), type=msg_type, status=True))
    except Exception as ex:
        logger.error(f"{msg_type} message didn't send for user #{uid1}, error: {ex}")


def care(client, user_repo, meet_repo, ntf_repo, config):
    while True:
        if config["devMode"]["enabled"]:
            weekday = int(config["devMode"]["weekday"])
            hour = int(config["devMode"]["hour"])
        else:
            weekday = date.today().weekday() + 1
            hour = int(time.strftime("%H"))

        season_id = season.get()
        ntf_dry_run = config["notifications"]["dryRun"]
        users = user_repo.list(spec={"pause_in_weeks": "0"})

        logger.info(f"Care about the current week. Today is {weekday} day of week ...")

        # NOTE: create meets
        if weekday < 5:
            meet_repo.create(
                uids=[user.id for user in users]
            )
        elif weekday == 5:
            if hour <= 13:
                meet_repo.create(
                    uids=[user.id for user in users],
                    additional_uids=config["bot"]["additionalUsers"]
                )

        meets = meet_repo.list(spec={"season": season_id})
        pairs = []

        # NOTE: Create pairs (it's the same as meets, but more convenient form)
        for meet in meets:
            unique_u1 = True
            unique_u2 = True

            if len(meet_repo.list({"season": season_id, "or": {"uid1": meet.uid1, "uid2": meet.uid1}})) > 1:
                unique_u1 = False
            if len(meet_repo.list({"season": season_id, "or": {"uid1": meet.uid2, "uid2": meet.uid2}})) > 1:
                unique_u2 = False

            pairs.append({
                "uid1": meet.uid1, "uid2": meet.uid2, "meet_id": meet.id, "unique": unique_u1
            })
            pairs.append({
                "uid1": meet.uid2, "uid2": meet.uid1, "meet_id": meet.id, "unique": unique_u2
            })

        # NOTE: notify users
        for pair in pairs:

            # NOTE: send info message
            if weekday <= 5:
                if pair['unique']:
                    info_msg = messages.MEET_INFO
                else:
                    info_msg = messages.MEET_INFO_NOT_UNIQUE

                msg_wrapper(
                    client=client, ntf_repo=ntf_repo, pair=pair,
                    msg_type=common.NTF_TYPES.info, msg_text=info_msg,
                    dry_run=ntf_dry_run
                )
            # NOTE: send reminder message
            if weekday >= 3:
                msg_wrapper(
                    client=client, ntf_repo=ntf_repo, pair=pair,
                    msg_type=common.NTF_TYPES.reminder, msg_text=messages.MEET_REMINDER,
                    dry_run=ntf_dry_run,
                    msg_blocks=elements.MEET_REMINDER, inline_msg_block=True
                )
            # NOTE: send feedback & next_week messages
            if weekday == 5:
                if 10 <= hour <= 16:
                    msg_wrapper(
                        client=client, ntf_repo=ntf_repo, pair=pair,
                        msg_type=common.NTF_TYPES.feedback, msg_text=messages.MEET_FEEDBACK,
                        dry_run=ntf_dry_run,
                        msg_blocks=elements.MEET_FEEDBACK, inline_msg_block=True
                    )
                elif hour >= 17:
                    msg_wrapper(
                        client=client, ntf_repo=ntf_repo, pair=pair,
                        msg_type=common.NTF_TYPES.next_week, msg_text=messages.MEET_NEXT,
                        dry_run=ntf_dry_run,
                        msg_blocks=elements.MEET_NEXT, inline_msg_block=True
                    )
        # NOTE: Change pause_in_weeks for all users
        if weekday == 7:
            for usr in user_repo.list():
                if int(usr.pause_in_weeks) > 0:
                    usr.pause_in_weeks = str(int(usr.pause_in_weeks) - 1)
                    user_repo.update(usr)

        time.sleep(config["daemons"]["week"]["poolPeriod"])
