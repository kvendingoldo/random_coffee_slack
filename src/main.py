# -*- coding: utf-8 -*-

import threading

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from loguru import logger
from mysql.connector import pooling

from entities import user
from utils import config, season

from daemons import week
from database.dao import meetDao, userDao, ratingDao
from database import exceptions
from database.interface import connector

config = config.load("../resources/config.yml", "../.env")
app = App(
    token=config["slack"]["botToken"]
)


@app.command("/help")
def flow_help(body, ack, say):
    logger.info("flow::help")
    ack()

    say(
        text=f"TODO"
    )


@app.command("/quit")
def flow_quit(body, ack, say):
    logger.info("flow::quit")

    uid = body['user_id']
    userDAO.delete_by_id(uid)
    ratingDAO.delete(uid)
    meetDAO.delete(uid)

    say(
        text=f"Sorry to see this decision. Hope to see you soon again. " \
             f"Just write /start again in this case. Information about you was deleted."
    )


@app.command("/start")
def flow_participate_0(body, ack, say):
    logger.info("flow::participate::0")

    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hi there!👋\n\n"
                            "I'm a Random Coffee bot here to help you create real connections with Grid Dynamis people worldwide. "
                            "Weekly I'll randomly pick one exciting person for you to catch up with. "
                            "You both will receive each other's names; "
                            "slack them, agree on a date and choose a platform to meet: zoom, skype, meet, etc. \n\n"
                            "So are you up for? \n\n"
                            "Enter Join to move forward."
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
                        "action_id": "flow_help"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Cancel"
                        },
                        "style": "danger",
                        "action_id": "flow_stop"
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

    usr = userDAO.get(body["user"]["id"])

    if usr.loc == "none":
        usr.loc = body["actions"][0]["selected_options"][0]["value"]
        userDAO.update(usr)

    flow_participate_2(ack, body, action, logr, client, say)


@app.action("flow_participate_1")
def flow_participate_1(ack, body, action, logr, client, say):
    logger.info("flow::participate::1 ::: ", body)
    ack()

    try:
        msg_user = userDAO.get(body["user"]["id"])
    except exceptions.NoResultFound as ex:
        new_user = user.User(username=body["user"]["username"], uid=body["user"]["id"])
        userDAO.add(new_user)
        ratingDAO.add(new_user.uid)

        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Tell me a little bit about yourself! \n\n" \
                            "What are you location?"
                }
            }
        ]

        attachments = [
            {
                "fallback": "Upgrade your Slack client to use messages like these.",
                "color": "3AA3E3",
                "attachment_type": "default",
                "callback_id": "location",
                "actions": [
                    {
                        "name": "Location",
                        "text": "You location",
                        "type": "select",
                        "options": [
                            {
                                "text": "Saratov",
                                "value": "saratov"
                            },
                            {
                                "text": "St. Petersburg",
                                "value": "spb"
                            },
                        ]
                    }
                ]
            }
        ]

        client.chat_update(
            channel=body['channel']['id'],
            ts=body['message']['ts'],
            attachments=attachments,
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
                "text": "Wow! Now you’re a Random coffee participant! \n\n" \
                        "What’s next? \n\n" \
                        "1. Every Monday you’ll receive a name of your next coffee partner \n" \
                        "2. Slack them, agree on a date and choose a platform to meet: zoom, skype, meet or even office in your location? \n" \
                        "3. Be interested and punctual. No one wants their coffee pause to be ruined."
            },
            "accessory": {
                "type": "image",
                "image_url": "https://image.freepik.com/free-vector/cute-unicorn-vector-with-donut-cartoon_70350-110.jpg",
                "alt_text": "cute donut"
            }
        }
    ]

    if "original_message" in body.keys():
        ts = body["original_message"]["ts"]
    else:
        ts = body["message"]["ts"]

    client.chat_update(
        channel=body['channel']['id'],
        ts=ts,
        attachments=[],
        blocks=blocks
    )


@app.action("flow_stop")
def flow_stop(body, ack, say):
    ack()
    say(
        text="I’m looking forward to seeing you when you come back"
    )

    usr = userDAO.get(body["user"]["id"])
    usr.pause_in_weeks = "inf"
    userDAO.update(usr)


@app.action("flow_next_week_yes")
def flow_next_week_yes(body, ack, say):
    ack()
    say(
        text="Great! Next Monday I’ll choose one more amazing coffee partner for you!"
    )

    usr = userDAO.get(body["user"]["id"])
    usr.pause_in_weeks = "0"
    userDAO.update(usr)


@app.action("flow_next_week_pause_1w")
def flow_next_week_pause_1w(body, ack, say):
    ack()

    usr = userDAO.get(body["user"]["id"])
    usr.pause_in_weeks = "1"
    userDAO.update(usr)

    say(
        text=f"I see. Let's do this again next week!"
    )


@app.action("flow_next_week_pause_1m")
def flow_next_week_pause_1m(body, ack, say):
    ack()

    usr = userDAO.get(body["user"]["id"])
    usr.pause_in_weeks = "4"
    userDAO.update(usr)

    say(
        text=f"I see. I will get back to you in a month!"
    )


@app.action("flow_meet_was")
def flow_meet_was(ack, body, action, logger, client, say):
    ack()

    uid = body["user"]["id"]

    partner_uid = meetDAO.get_partner_uid(
        season.get_current(), uid
    )

    ratingDAO.change(uid, partner_uid, 0.1)

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Thank you for response!"
            }
        }
    ]

    client.chat_update(
        channel=body['channel']['id'],
        ts=body["message"]["ts"],
        attachments=[],
        blocks=blocks
    )


@app.action("flow_meet_was_not")
def flow_meet_was_not(ack, body, action, logger, client, say):
    ack()

    uid = body["user"]["id"]

    partner_uid = meetDAO.get_partner_uid(
        season.get_current(), uid
    )

    ratingDAO.change(uid, partner_uid, -0.1)

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Thank you for response!"
            }
        }
    ]

    client.chat_update(
        channel=body['channel']['id'],
        ts=body["message"]["ts"],
        attachments=[],
        blocks=blocks
    )


@app.action("flow_meet_had")
def flow_meet_was_not(ack, body, action, logger, client, say):
    ack()

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":eyes: How it was?"
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
        ts=body["message"]["ts"],
        attachments=[],
        blocks=blocks
    )


@app.message("update_profile")
def update_profile(ack, body, action, logger, client, say):
    logger.info("flow::update_profile :::", body)

    ack()

    blocks = [
        {
            "dispatch_action": True,
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "plain_text_input-action"
            },
            "label": {
                "type": "plain_text",
                "text": "Instagram",
                "emoji": True
            }
        },
        {
            "dispatch_action": True,
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "plain_text_input-action"
            },
            "label": {
                "type": "plain_text",
                "text": "Telegram",
                "emoji": True
            }
        },
        {
            "dispatch_action": True,
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "plain_text_input-action"
            },
            "label": {
                "type": "plain_text",
                "text": "VK",
                "emoji": True
            }
        },
        {
            "dispatch_action": True,
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "plain_text_input-action"
            },
            "label": {
                "type": "plain_text",
                "text": "Facebook",
                "emoji": True
            }
        }
    ]

    # client.chat_update(channel=body['channel']['id'],
    #                    ts=body["message"]["ts"],
    #                    attachments=[],
    #                    blocks=blocks)


if __name__ == "__main__":
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

    week = threading.Thread(
        target=week.care,
        args=(app.client, userDAO, meetDAO, config,)
    )
    week.start()

    bot = threading.Thread(target=SocketModeHandler(app, config["slack"]["appToken"]).start(), args=())
    bot.start()

    # week.join()
    # bot.join()
