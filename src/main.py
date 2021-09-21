# -*- coding: utf-8 -*-

import threading

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from loguru import logger
from mysql.connector import pooling

from entities import user
from utils import config, season

from daemons import week
from database.dao import meetDao, userDao, ratingDao, notificationDao
from database import exceptions
from database.interface import connector
from constants import messages, elements
from utils import msg

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
                _ = userDAO.get_by_id(body["user_id"])
            except exceptions.NoResultFound:
                ack()
                say(text=messages.USER_NOT_FOUND)
            else:
                flow_stop(ack, body)
        else:
            ack()
            say(text=messages.COMMAND_NOT_FOUND)


@app.action("help")
def action_help(ack, body, client, say):
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
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": messages.FLOW_STOP
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


@app.event("message")
def handle_message_events(body, logger):
    logger.info("Handled message event, body: ", body)


def flow_quit(body, ack, say):
    logger.info("flow::quit")

    uid = body['user_id']
    userDAO.delete_by_id(uid)
    ratingDAO.delete_by_id(uid)
    meetDAO.delete_by_id(uid)

    ack()
    say(text=messages.FLOW_QUIT)


def flow_participate_0(body, ack, say):
    logger.info("flow::participate::0")

    ack()
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": messages.FLOW_PARTICIPATE_0
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://image.freepik.com/free-vector/cute-unicorn-vector-with-donut-cartoon_70350-110.jpg",
                    "alt_text": "cute donut"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Join"
                        },
                        "style": "primary",
                        "action_id": "flow_participate_1"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Help"
                        },
                        "action_id": "help"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Cancel"
                        },
                        "style": "danger",
                        "action_id": "stop"
                    }
                ]
            }
        ],
        text=""
    )


@app.action("location")
def location(ack, body, action, logr, client, say):
    logger.info("flow::location")
    ack()

    usr = userDAO.get_by_id(body["user"]["id"])

    if usr.loc == "none":
        usr.loc = body["actions"][0]["selected_option"]["value"]
        userDAO.update(usr)

    flow_participate_2(ack, body, action, logr, client, say)


@app.action("flow_participate_1")
def flow_participate_1(ack, body, action, logr, client, say):
    logger.info("flow::participate::1 ::: ", body)
    ack()

    try:
        msg_user = userDAO.get_by_id(body["user"]["id"])
    except exceptions.NoResultFound as ex:
        new_user = user.User(username=body["user"]["username"], uid=body["user"]["id"], pause_in_weeks="0")

        userDAO.add(new_user)
        ratingDAO.add_by_id(new_user.uid)

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
            blocks=blocks
        )
    else:
        flow_participate_2(ack, body, action, logr, client, say)


@app.action("flow_participate_2")
def flow_participate_2(ack, body, action, logr, client, say):
    logger.info("flow::participate::2 ::: ", body)
    ack()

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": messages.FLOW_PARTICIPATE_2
            },
            "accessory": {
                "type": "image",
                "image_url": "https://image.freepik.com/free-vector/cute-unicorn-vector-with-donut-cartoon_70350-110.jpg",
                "alt_text": "cute donut"
            }
        }
    ]

    client.chat_update(
        channel=body['channel']['id'],
        ts=msg.get_ts(body),
        blocks=blocks
    )


@app.action("flow_next_week_yes")
def flow_next_week_yes(ack, body, action, logr, client, say):
    ack()

    usr = userDAO.get_by_id(body["user"]["id"])
    usr.pause_in_weeks = "0"
    userDAO.update(usr)

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

    usr = userDAO.get_by_id(body["user"]["id"])
    usr.pause_in_weeks = period
    userDAO.update(usr)

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
def flow_next_week_pause_1w(ack, body, client, say):
    stop_wrapper(ack, body, client, "1", messages.FLOW_WEEK_PAUSE_1W)


@app.action("flow_next_week_pause_1m")
def flow_next_week_pause_1m(ack, body, client, say):
    stop_wrapper(ack, body, client, "1", messages.FLOW_WEEK_PAUSE_1M)


@app.action("stop")
def action_stop(ack, body, client, say):
    stop_wrapper(ack, body, client, "inf", messages.ACTION_STOP)


@app.action("flow_meet_was")
def flow_meet_was(ack, body, action, logger, client, say):
    ack()

    uid = body["user"]["id"]

    partner_uid = meetDAO.get_uid2_by_id(
        season.get(), uid
    )

    ratingDAO.change_by_ids(uid, partner_uid, 0.1)

    client.chat_update(
        channel=body['channel']['id'],
        ts=msg.get_ts(body),
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": messages.FLOW_MEET_WAS
                }
            }
        ]
    )


@app.action("flow_meet_was_not")
def flow_meet_was_not(ack, body, action, logger, client, say):
    ack()

    uid = body["user"]["id"]

    partner_uid = meetDAO.get_uid2_by_id(
        season.get(), uid
    )

    ratingDAO.change_by_ids(uid, partner_uid, -0.1)

    client.chat_update(
        channel=body['channel']['id'],
        ts=msg.get_ts(body),
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": messages.FLOW_MEET_WASNT

                }
            }
        ]
    )


@app.action("flow_meet_had")
def flow_meet_had(ack, body, action, logger, client, say):
    ack()

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": messages.FLOW_MEET_HAD
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
                        "text": "Awesome!"
                    },
                    "style": "primary",
                    "action_id": "flow_meet_was"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Could be better"
                    },
                    "style": "primary",
                    "action_id": "flow_meet_was_not"
                }
            ]
        }
    ]

    client.chat_update(
        channel=body['channel']['id'],
        ts=msg.get_ts(body),
        blocks=blocks
    )


if __name__ == "__main__":
    logger.info("Bot launching ...")

    connection_pool = pooling.MySQLConnectionPool(
        pool_name="default",
        pool_size=5,
        pool_reset_session=True,
        host=config["database"]["host"],
        port=config["database"]["port"],
        database=config["database"]["db"],
        user=config["database"]["username"],
        password=config["database"]["password"]
    )

    connector = connector.Connector(connection_pool)

    userDAO = userDao.UserDAO(connector)
    meetDAO = meetDao.MeetDao(connector)
    ratingDAO = ratingDao.RatingDao(connector)
    notificationDAO = notificationDao.NotificationDao(connector)

    week = threading.Thread(
        target=week.care,
        args=(app.client, userDAO, meetDAO, notificationDAO, config,)
    )
    week.start()

    bot = threading.Thread(target=SocketModeHandler(app, config["slack"]["appToken"]).start(), args=())
    bot.start()

    # week.join()
    # bot.join()
