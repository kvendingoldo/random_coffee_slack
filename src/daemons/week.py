# -*- coding: utf-8 -*-

import time

from datetime import date
from loguru import logger
from utils import season, repo, msg
from constants import messages, elements, common


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
                if len([pair for pair in pairs if pair.get('uid1') == meet.uid1]) > 0:
                    unique_u1 = False

            if len(meet_repo.list({"season": season_id, "or": {"uid1": meet.uid2, "uid2": meet.uid2}})) > 1:
                if len([pair for pair in pairs if pair.get('uid2') == meet.uid2]) > 0:
                    unique_u2 = False

            pairs.append({
                "uid1": meet.uid1, "uid2": meet.uid2, "meet_id": meet.id, "unique": unique_u1
            })
            pairs.append({
                "uid1": meet.uid2, "uid2": meet.uid1, "meet_id": meet.id, "unique": unique_u2
            })

        # NOTE: notify users
        for pair in pairs:
            msg_type_suffix = "" if pair['unique'] else "_NU"

            # NOTE: send info message
            if weekday <= 5:
                info_msg = messages.MEET_INFO if pair['unique'] else messages.MEET_INFO_NOT_UNIQUE

                msg.wrapper_user(
                    client=client,
                    ntf_repo=ntf_repo,
                    uid=pair["uid1"],
                    msg_type=common.NTF_TYPES.info + msg_type_suffix,
                    msg_text=info_msg.format(pair["uid2"]),
                    dry_run=ntf_dry_run
                )
            # NOTE: send reminder message
            if 3 <= weekday <= 5:
                msg.wrapper_user(
                    client=client,
                    ntf_repo=ntf_repo,
                    uid=pair["uid1"],
                    msg_type=common.NTF_TYPES.reminder + msg_type_suffix,
                    msg_text=(messages.MEET_REMINDER).format(pair["uid2"]),
                    dry_run=ntf_dry_run,
                    msg_blocks=elements.MEET_REMINDER,
                    inline_msg_block=True
                )
            # NOTE: send feedback & next_week messages
            if weekday == 5:
                if 10 <= hour <= 16:
                    msg.wrapper_user(
                        client=client,
                        ntf_repo=ntf_repo,
                        uid=pair["uid1"],
                        msg_type=common.NTF_TYPES.feedback + msg_type_suffix,
                        msg_text=(messages.MEET_FEEDBACK).format(pair["uid2"]),
                        dry_run=ntf_dry_run,
                        msg_blocks=elements.MEET_FEEDBACK,
                        inline_msg_block=True
                    )

        # NOTE: Ask about the next week
        if weekday == 5:
            for usr in user_repo.list():
                if usr.pause_in_weeks != "inf":
                    pause = int(usr.pause_in_weeks)

                    # Decrement pause for users who have pause > 1 week
                    if pause > 1:
                        usr.pause_in_weeks = str(pause - 1)
                        user_repo.update(usr)
                    else:
                        # Notify users who have pause = 0 | 1 week about the next week
                        if hour >= 17:
                            if pause == 1:
                                msg_text = messages.MEET_NEXT_AFTER_PAUSE
                                msg_blocks = elements.MEET_NEXT_AFTER_PAUSE
                            elif pause == 0:
                                msg_text = messages.MEET_NEXT
                                msg_blocks = elements.MEET_NEXT

                            msg.wrapper_user(
                                client=client, ntf_repo=ntf_repo, uid=usr.id,
                                msg_type=common.NTF_TYPES.next_week, msg_text=msg_text,
                                dry_run=ntf_dry_run,
                                msg_blocks=msg_blocks, inline_msg_block=True
                            )

        time.sleep(config["daemons"]["week"]["poolPeriod"])
