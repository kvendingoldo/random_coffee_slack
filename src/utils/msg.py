# -*- coding: utf-8 -*-

import re
import pytz
import datetime

from loguru import logger

from utils import season
from utils import time as utils_time
from models.notification import Notification
from db.exceptions import NotificationNotFoundError


def get_ts(body):
    if "original_message" in body.keys():
        ts = body["original_message"]["ts"]
    else:
        ts = body["message"]["ts"]

    return ts


def get_uid(text):
    uid = re.sub("<@|>", "", re.findall(r'(<@.*>)', text)[0])

    return uid


def send_msg_pair(client, pair, dry_run, msg_text, msg_blocks, inline_msg_block):
    uid1 = pair["uid1"]
    uid2 = pair["uid2"]

    if dry_run:
        logger.info("[DRY-RUN]:\n" + msg_text.format(uid2))
    else:
        if inline_msg_block:
            client.chat_postMessage(
                channel=uid1,
                text="You have a new notification in the chat",
                blocks=[{
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": msg_text.format(uid2)
                    },

                }] + msg_blocks
            )
        else:
            # TODO: probably it would be better to use inline for this case
            client.chat_postMessage(
                channel=uid1, text=msg_text.format(uid2), blocks=msg_blocks
            )


def send_msg_user(client, uid, dry_run, msg_text, msg_blocks, inline_msg_block):
    if dry_run:
        logger.info("[DRY-RUN]:\n" + msg_text)
    else:
        if inline_msg_block:
            client.chat_postMessage(
                channel=uid,
                text="You have a new notification in the chat",
                blocks=[{
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": msg_text
                    },

                }] + msg_blocks
            )
        else:
            # TODO: probably it would be better to use inline for this case
            client.chat_postMessage(
                channel=uid, text=msg_text, blocks=msg_blocks
            )


def wrapper_user(client, ntf_repo, usr_info, msg_type, msg_text, dry_run=True, msg_blocks=None, inline_msg_block=False):
    if msg_blocks is None:
        msg_blocks = []

    uid = usr_info["user"]["id"]
    user_name = usr_info["user"]["name"]

    try:
        offset = usr_info["user"]["tz_offset"]
    except KeyError:
        tz = pytz.timezone('Asia/Calcutta')
        dt = datetime.datetime.utcnow()
        offset = tz.utcoffset(dt).seconds

        logger.error(f"Failed to take tz_offset for {uid}; Standard {offset} will use used")

    user_time = utils_time.get_current_time(offset)

    try:
        ntf = ntf_repo.get({"uid": uid, "type": msg_type, "season": season.get()})
    except NotificationNotFoundError as ex:
        logger.error(ex)
        ntf = Notification(uid=uid, season=season.get(), type=msg_type, status=False)
        ntf_repo.add(ntf)
    except Exception as ex:
        logger.error(
            f"{msg_type} message didn't send for user {user_name} ({uid}). User time is {user_time}. Error: {ex}")
        return

    if ntf.status:
        logger.info(f"User {user_name} ({uid}) has already notified about {msg_type}. User time is {user_time}.")
    else:
        send_msg_user(client, uid, dry_run, msg_text, msg_blocks, inline_msg_block)
        ntf.status = True
        ntf_repo.update(ntf)
        logger.info(f"{msg_type} message sent for {user_name} ({uid}); User time is {user_time}.")


def generate_locations(locations):
    result = []
    for location in locations:
        result.append(
            {
                "text": {
                    "type": "plain_text",
                    "text": locations[location]["displayName"],
                    "emoji": True
                },
                "value": location
            }
        )
    return result


def generate_groups(groups):
    result = []
    for group in groups:
        result.append(
            {
                "text": {
                    "type": "plain_text",
                    "text": group["displayName"],
                    "emoji": True
                },
                "value": group["name"]
            }
        )
    return result


def generate_help_msg_block(commands):
    res = [{"type": "section", "text": {"type": "mrkdwn", "text": ":rcb: *List of Random Coffee Bot commands*"}}]

    for command in commands:
        res.append(
            {"type": "section", "text": {"type": "mrkdwn", "text": f"{command[0]}"}}
        )
        res.append(
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://api.slack.com/img/blocks/bkb_template_images/tripAgentLocationMarker.png",
                        "alt_text": "Command description"
                    },
                    {
                        "type": "plain_text",
                        "emoji": True,
                        "text": command[1]
                    }
                ]
            }
        )
        res.append({"type": "divider"})

    res.append({"type": "context",
                "elements": [{"type": "mrkdwn", "text": "❓If you have any questions contact @asharov or @ytsvetkova"}]})

    return res
