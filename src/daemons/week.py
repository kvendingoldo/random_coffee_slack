# -*- coding: utf-8 -*-

import time

from loguru import logger
from utils import season, repo, msg, groups
from utils import config as cfg_utils
from utils import time as utils_time
from constants import messages, elements, common
from db import utils as db_utils
from db.exceptions import NotificationNotFoundError
from models.notification import Notification


def care(client, config):
    user_repo, ntf_repo, rating_repo, meet_repo, metadata_repo = db_utils.get_repos(config)

    while True:
        config_meet_groups = config["generated"]["groups"]
        weekday, internal_bot_hour = cfg_utils.get_week_info(config)

        season_id = season.get()
        ntf_dry_run = config["notifications"]["dryRun"]
        users = user_repo.list(spec={"pause_in_weeks": "0"})

        logger.info(f"Care about the current week. Today is {weekday} day of week ...")

        # NOTE: create meets
        if weekday <= 3:
            for m_group in repo.get_unique_meet_groups(users):
                if weekday == 3:
                    additional_uids = groups.get_group_additional_users(m_group, config_meet_groups)
                else:
                    additional_uids = []

                if groups.check_group_enabled(group=m_group, groups=config_meet_groups):
                    meet_repo.create(
                        uids=[user.id for user in users if user.meet_group == m_group],
                        additional_uids=additional_uids
                    )

        users_with_pair = set()
        meets = meet_repo.list(spec={"season": season_id})
        pairs = []

        # NOTE: Create pairs (it's the same as meets, but more convenient form)
        for meet in meets:
            users_with_pair.add(meet.uid1)
            users_with_pair.add(meet.uid2)

            unique_u1 = True
            unique_u2 = True

            if len(meet_repo.list({"season": season_id, "or": {"uid1": meet.uid1, "uid2": meet.uid1}})) > 1:
                if len([pair for pair in pairs if pair.get('uid1') == meet.uid1]) > 0:
                    unique_u1 = False

            if len(meet_repo.list({"season": season_id, "or": {"uid1": meet.uid2, "uid2": meet.uid2}})) > 1:
                if len([pair for pair in pairs if pair.get('uid2') == meet.uid2]) > 0:
                    unique_u2 = False

            pairs.append({
                "uid1": meet.uid1, "uid2": meet.uid2, "meet_id": meet.id, "unique": unique_u1, "is_host": True
            })
            pairs.append({
                "uid1": meet.uid2, "uid2": meet.uid1, "meet_id": meet.id, "unique": unique_u2, "is_host": False
            })

        #
        # FLOW: Notify users about week events
        #
        for pair in pairs:
            msg_type_suffix = "" if pair['unique'] else "_NU"

            usr_info = client.users_info(user=pair["uid1"])

            try:
                hour = utils_time.get_current_hour(usr_info["user"]["tz_offset"])
            except KeyError:
                logger.error(f"Failed to take tz_offset for {pair['uid1']}")
                hour = internal_bot_hour

            #
            # FLOW: send info message
            #
            if weekday <= 5:
                info_msg = messages.MEET_INFO if pair['unique'] else messages.MEET_INFO_NOT_UNIQUE

                if pair['is_host']:
                    info_msg = f"{info_msg} \n {messages.MEET_HOST}"
                else:
                    info_msg = f"{info_msg} \n {messages.MEET_NOT_HOST}"

                msg.wrapper_user(
                    client=client,
                    ntf_repo=ntf_repo,
                    usr_info=usr_info,
                    msg_type=common.NTF_TYPES.info + msg_type_suffix,
                    msg_text=info_msg.format(pair["uid2"]),
                    dry_run=ntf_dry_run
                )

            #
            # FLOW: send reminder message
            #
            if 3 <= weekday <= 4:
                msg.wrapper_user(
                    client=client,
                    ntf_repo=ntf_repo,
                    usr_info=usr_info,
                    msg_type=common.NTF_TYPES.reminder + msg_type_suffix,
                    msg_text=(messages.MEET_REMINDER).format(pair["uid2"]),
                    dry_run=ntf_dry_run,
                    msg_blocks=elements.MEET_REMINDER,
                    inline_msg_block=True
                )

            #
            # FLOW: ask user feedback
            #
            if weekday == 5:
                if 16 <= hour <= 20:
                    msg.wrapper_user(
                        client=client,
                        ntf_repo=ntf_repo,
                        usr_info=usr_info,
                        msg_type=common.NTF_TYPES.feedback + msg_type_suffix,
                        msg_text=(messages.MEET_FEEDBACK).format(pair["uid2"]),
                        dry_run=ntf_dry_run,
                        msg_blocks=elements.MEET_FEEDBACK,
                        inline_msg_block=True
                    )

        #
        # FLOW: notify users who do not have a pair
        #       we're trying to send notification about next week from Mon to Fri before 1AM
        #       after Fri 1AM unsuccessful search message will be sent
        #
        if 1 <= weekday <= 5:
            for usr in users:
                usr_info = client.users_info(user=usr.id)

                try:
                    hour = utils_time.get_current_hour(usr_info["user"]["tz_offset"])
                except KeyError:
                    logger.error(f"Failed to take tz_offset for {usr.id}")
                    hour = internal_bot_hour

                if hour <= 13:
                    message = messages.MEET_LOOKING
                elif 16 > hour > 13:
                    if weekday == 5:
                        message = messages.MEET_UNSUCCESSFUL_SEARCH
                    else:
                        continue
                else:
                    continue

                if usr.id not in users_with_pair:
                    if not groups.check_group_enabled(group=usr.meet_group, groups=config_meet_groups):
                        message = messages.FLOW_PARTNER_GROUP_DISABLED.format(usr.meet_group)

                    msg.wrapper_user(
                        client=client,
                        ntf_repo=ntf_repo,
                        usr_info=usr_info,
                        msg_type=common.NTF_TYPES.looking,
                        msg_text=message,
                        dry_run=ntf_dry_run
                    )

        #
        # FLOW: Ask users about the next week
        #
        if weekday == 5:
            for usr in user_repo.list():
                if usr.pause_in_weeks != "inf":
                    pause = int(usr.pause_in_weeks)

                    # Decrement pause for users who have pause > 1 week
                    if pause > 1:
                        msg_type = common.NTF_TYPES.next_week
                        try:
                            ntf = ntf_repo.get({"uid": usr.id, "type": msg_type, "season": season.get()})
                            logger.info(
                                f"User {usr.username} ({usr.id}) has already notified about {msg_type}; pause_in_weeks has already decremented to {usr.pause_in_weeks}")
                        except NotificationNotFoundError:
                            logger.error(
                                f"Notification about {msg_type} hasn't found for {usr.username} ({usr.id}). Will be added now as well as pause_in_weeks will be decremented."
                            )
                            ntf = Notification(uid=usr.id, season=season.get(), type=msg_type, status=False)
                            ntf_repo.add(ntf)

                            usr.pause_in_weeks = str(pause - 1)
                            user_repo.update(usr)
                        except Exception as ex:
                            logger.error(
                                f"{msg_type} message didn't send for user {usr.username} ({usr.id}). Error: {ex}")
                    else:
                        usr_info = client.users_info(user=usr.id)

                        try:
                            hour = utils_time.get_current_hour(usr_info["user"]["tz_offset"])
                        except KeyError:
                            logger.error(f"Failed to take tz_offset for {usr.id}")
                            hour = internal_bot_hour

                        # Notify users who have "pause" = 0 or 1 week about the next week
                        if hour > 16:
                            if pause == 1:
                                msg_text = messages.MEET_NEXT_AFTER_PAUSE
                                msg_blocks = elements.MEET_NEXT_AFTER_PAUSE
                            elif pause == 0:
                                msg_text = messages.MEET_NEXT
                                msg_blocks = elements.MEET_NEXT

                            msg.wrapper_user(
                                client=client,
                                ntf_repo=ntf_repo,
                                usr_info=usr_info,
                                msg_type=common.NTF_TYPES.next_week, msg_text=msg_text,
                                dry_run=ntf_dry_run,
                                msg_blocks=msg_blocks, inline_msg_block=True
                            )

        time.sleep(config["daemons"]["week"]["poolPeriod"])
