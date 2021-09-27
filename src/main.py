# -*- coding: utf-8 -*-

import threading
import os

from datetime import datetime

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from loguru import logger

from utils import config, season

from daemons import week

from constants import messages, elements
from utils import msg

from db import database
from db.exceptions import UserNotFoundError, RatingNotFoundError
from db.repo.user import UserRepository
from db.repo.notification import NotificationRepository
from db.repo.rating import RatingRepository
from db.repo.meet import MeetRepository

from models.user import User
from models.rating import Rating

config = config.load("../resources/config.yml")
app = App(
    token=config["slack"]["botToken"]
)


@app.command("/rcb")
def rcb_command(body, ack, say):
    msg = body["text"]
    if msg:
        if msg == "start":
            flow_participate_0(body, ack, say)
        elif msg == "help":
            ack()
            say(text=messages.FLOW_HELP)
        elif msg == "quit":
            flow_quit(body, ack, say)
        elif msg == "stop":
            try:
                _ = user_repo.get_by_id(body["user_id"])
            except UserNotFoundError:
                ack()
                say(text=messages.USER_NOT_FOUND)
            else:
                flow_stop(ack, body)
        else:
            ack()
            say(text=messages.COMMAND_NOT_FOUND)


@app.action("help")
def action_help(ack, body, client):
    logger.info("flow::help")

    ack()
    client.chat_update(
        channel=body['channel']['id'],
        ts=msg.get_ts(body),
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": messages.FLOW_HELP
                }
            }
        ]
    )


def flow_stop(ack, body):
    ack()
    app.client.chat_postMessage(
        channel=body["user_id"],
        text="",
        blocks=[{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": messages.FLOW_STOP
            },
        }] + elements.FLOW_STOP
    )


@app.event("message")
def handle_message_events(body, say):
    pass
    # logger.debug(f"Handled message event, body: {body}")
    # TODO
    # if body["event"]["type"] == "message":
    #     say(text=messages.COMMAND_NOT_FOUND)


def flow_quit(body, ack, say):
    uid = body['user_id']

    logger.info(f"flow::quit for user {uid}")
    user_repo.delete_by_id(uid)

    ack()
    say(text=messages.FLOW_QUIT)


def flow_participate_0(body, ack, say):
    logger.info(f"flow::participate::0 for user {body['user_id']}")

    ack()
    # TODO: replace to client
    say(
        blocks=[{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": messages.FLOW_PARTICIPATE_0
            },
            "accessory": elements.DONUT
        }] + elements.FLOW_PART_0
    )


@app.action("location")
def location(ack, body, client):
    logger.info(f"flow::location for user {body['user']['id']}")

    ack()

    usr = user_repo.get_by_id(body["user"]["id"])

    if usr.loc == "none":
        usr.loc = body["actions"][0]["selected_option"]["value"]
        user_repo.update(usr)

    flow_participate_2(ack, body, client)


@app.action("flow_participate_1")
def flow_participate_1(ack, body, client):
    uid = body["user"]["id"]

    logger.info(f"flow::participate::1 for user {uid}")
    ack()

    try:
        msg_user = user_repo.get_by_id(uid)
        msg_user.pause_in_weeks = "0"

        user_repo.update(msg_user)
    except UserNotFoundError as ex:
        new_user = User(id=uid, username=body["user"]["username"], pause_in_weeks="0")

        user_repo.add(new_user)
        rating_repo.add(new_user.id)

        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": messages.FLOW_PARTICIPATE_1
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True
                    },
                    "options": elements.LOCATIONS,
                    "action_id": "location"
                }
            }
        ]

        client.chat_update(
            channel=body['channel']['id'],
            ts=msg.get_ts(body),
            text="",
            blocks=blocks
        )

    flow_participate_2(ack, body, client)


@app.action("flow_participate_2")
def flow_participate_2(ack, body, client):
    logger.info(f"flow::participate::2 for user {body['user']['id']}")

    ack()

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": messages.FLOW_PARTICIPATE_2
            },
            "accessory": elements.DONUT
        }
    ]

    client.chat_update(
        channel=body['channel']['id'],
        ts=msg.get_ts(body),
        blocks=blocks
    )


@app.action("flow_next_week_yes")
def flow_next_week_yes(ack, body, client):
    ack()

    usr = user_repo.get_by_id(body["user"]["id"])
    usr.pause_in_weeks = "0"
    user_repo.update(usr)

    client.chat_update(
        channel=body['channel']['id'],
        ts=msg.get_ts(body),
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": messages.FLOW_WEEK_YES

                }
            }
        ]
    )


def stop_wrapper(ack, body, client, period, message):
    ack()

    usr = user_repo.get_by_id(body["user"]["id"])
    usr.pause_in_weeks = period
    user_repo.update(usr)

    client.chat_update(
        channel=body['channel']['id'],
        ts=msg.get_ts(body),
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }
        ]
    )


@app.action("flow_next_week_pause_1w")
def flow_next_week_pause_1w(ack, body, client):
    stop_wrapper(ack, body, client, "1", messages.FLOW_WEEK_PAUSE_1W)


@app.action("flow_next_week_pause_1m")
def flow_next_week_pause_1m(ack, body, client):
    stop_wrapper(ack, body, client, "4", messages.FLOW_WEEK_PAUSE_1M)


@app.action("stop")
def action_stop(ack, body, client):
    stop_wrapper(ack, body, client, "inf", messages.ACTION_STOP)


def flow_meet_rate(ack, body, client, sign):
    ack()

    uid1 = body["user"]["id"]
    uid2 = msg.get_uid(body['message']['blocks'][0]['text']['text'])
    season_id = season.get()

    # TODO: add error handling
    meet = (meet_repo.list(spec={"season": season_id, "uid1": uid1, "uid2": uid2}) + \
            meet_repo.list(spec={"season": season_id, "uid2": uid1, "uid1": uid2}))[0]
    meet.completed = True
    meet_repo.update(meet)

    try:
        rating = rating_repo.get_by_ids(uid1, uid2)
    except RatingNotFoundError:
        rating = Rating(uid1=uid1, uid2=uid2, rating=1.0)

    if sign == "+":
        rating.value += 0.1
    else:
        rating.value -= 0.1
    rating_repo.update(rating)

    client.chat_update(
        channel=body['channel']['id'],
        ts=msg.get_ts(body),
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": messages.FLOW_MEET_RATE
                }
            }
        ]
    )


@app.action("flow_meet_was")
def flow_meet_was(ack, body, client):
    flow_meet_rate(ack, body, client, "+")


@app.action("flow_meet_was_not")
def flow_meet_was_not(ack, body, client):
    flow_meet_rate(ack, body, client, "-")


@app.action("flow_meet_had")
def flow_meet_had(ack, body, client):
    uid2 = msg.get_uid(body['message']['blocks'][0]['text']['text'])
    ack()

    blocks = [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (messages.FLOW_MEET_HAD).format(uid2)
        },

    }] + elements.MEET_HAD

    client.chat_update(
        channel=body['channel']['id'],
        ts=msg.get_ts(body),
        blocks=blocks
    )


if __name__ == "__main__":
    log_dir = os.getenv("RCB_LOG_DIR")

    logger.add(f"{log_dir}/{datetime.today().strftime('%Y-%m-%d-%H:%M')}.log", level="INFO")

    logger.info("Bot launching ...")

    db_url = "mysql://{}:{}@{}:{}/{}".format(
        config["database"]["username"], config["database"]["password"],
        config["database"]["host"], config["database"]["port"],
        config["database"]["db"]
    )

    db = database.Database(db_url)
    db.create_database()

    user_repo = UserRepository(session_factory=db.session)
    ntf_repo = NotificationRepository(session_factory=db.session)
    rating_repo = RatingRepository(session_factory=db.session)
    meet_repo = MeetRepository(session_factory=db.session)

    week = threading.Thread(
        target=week.care,
        args=(app.client, user_repo, meet_repo, ntf_repo, config,)
    )
    week.start()

    bot = threading.Thread(target=SocketModeHandler(app, config["slack"]["appToken"]).start(), args=())
    bot.start()

    # week.join()
    # bot.join()
