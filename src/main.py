# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join

from slack_bolt import App
from loguru import logger
import threading
from daemons import pairs, week
from database.dao import meets, users
from database.interface import connector
from entities import user
from utils import config
from mysql.connector import pooling

config = config.load("../config.yml")
app = App(
    token=config["slack"]["otoken"],
    signing_secret=config["slack"]["sigSecret"],
)


#
# Bot flow
#
@app.action("flow_help")
def flow_help(body, ack, say):
    ack()
    say(
        text=f"TODO: Add some help info"
    )


@app.message("start")
def flow_participate_0(message, say):
    logger.info("flow::participate::0")
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hi there!👋\n\n" \
                            "I'm a Random Coffee bot here to help you create real connections with Grid Dynamis people worldwide. Weekly I'll randomly pick one exciting person for you to catch up with. You both will receive each other's names; slack them, agree on a date and choose a platform to meet: zoom, skype, meet, etc.\n\n" \
                            "So are you up for?\n\n" \
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
def location(body, ack, say):
    location = body["actions"][0]["selected_options"][0]["value"]

    logger.info("location :::", location)

    ack()

    if usersDAO.get_user(body["user"]["id"]).loc == "none":
        usersDAO.set_loc(user.User(username=body["user"]["name"],
                                   uid=body["user"]["id"],
                                   loc=location))

    flow_participate_2(body, ack, say)


@app.action("flow_participate_1")
def flow_participate_1(body, ack, say):
    logger.info("flow::participate::1 :::", body)

    msg_user = usersDAO.get_user(body["user"]["id"])

    print(msg_user)
    print(msg_user.loc)

    if not msg_user or msg_user.loc == "none":
        usersDAO.add(user.User(username=body["user"]["username"], uid=body["user"]["id"]))

        # TODO: get links from user
        ack()
        say(
            text="",
            attachments=[
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
                            ],
                        }
                    ]
                }
            ],
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Tell me a little bit about yourself!\n\n" \
                                "What are you into?\n\n" \
                                "Share links on your Instagram or Facebook if any.",
                    },
                }

            ]
        )
    else:
        flow_participate_2(body, ack, say)


@app.action("flow_participate_2")
def flow_participate_2(body, ack, say):
    logger.info("flow::participate::2 :::", body)

    ack()
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Wow! Now you’re a Random coffee participant!\n\n" \
                            "What’s next?\n\n" \
                            "1. Every Monday you’ll receive a name of your next coffee partner\n" \
                            "2. Slack them, agree on a date and choose a platform to meet: zoom, skype, meet or even office in your location?\n" \
                            "3. Be interested and punctual. No one wants their coffee pause to be ruined."
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://image.freepik.com/free-vector/cute-unicorn-vector-with-donut-cartoon_70350-110.jpg",
                    "alt_text": "cute donut"
                }
            }
        ],
        text=""
    )


@app.action("flow_stop")
def flow_stop(body, ack, say):
    logger.info("flow::participate::cancel :::", body)

    ack()
    say(
        text=f" I’m looking forward to seeing you when you come back"
    )


@app.action("flow_next_week_yes")
def flow_next_week_yes(body, ack, say):
    ack()
    say(
        text=f"Great! Next Monday I’ll choose one more amazing coffee partner for you!"
    )

    # TODO
    # user.ready = True
    # users.set_ready(connection, user)


@app.action("flow_next_week_pause_1w")
def flow_next_week_pause_1w(body, ack, say):
    ack()
    say(
        text=f"I see. Let's do this again next week!"
    )

    # user.ready = False
    # users.set_ready(connection, user)


@app.action("flow_next_week_pause_1m")
def flow_next_week_pause_1m(body, ack, say):
    ack()
    say(
        text=f"I see. I will get back to you in a month!"
    )

    # user.ready = False
    # users.set_ready(connection, user)


@app.action("flow_meet_was")
def flow_meet_was(body, ack, say):
    ack()
    say(
        text=f"TODO: flow_meet_was"
    )

    # TODO: do some calculation stuff


@app.action("flow_meet_was_not")
def flow_meet_was_not(body, ack, say):
    ack()
    say(
        text=f"TODO: flow_meet_was_not"
    )

    # TODO: do some calculation stuff


if __name__ == "__main__":
    connection_pool = pooling.MySQLConnectionPool(pool_name="default",
                                                  pool_size=5,
                                                  pool_reset_session=True,
                                                  host=config["database"]["host"],
                                                  port=config["database"]["port"],
                                                  database=config["database"]["db"],
                                                  user=config["database"]["username"],
                                                  password=config["database"]["password"]
                                                  )

    connector = connector.Connector(connection_pool)

    usersDAO = users.UsersDAO(connector)
    meetsDAO = meets.MeetsDao(connector)
    # usersDAO.get_user("uid")
    # logger.info(list(usersDAO.pairs()))
    # pairs = threading.Thread(target=pairs.create, args=(app.client, connection_pool, 5,))
    # pairs.start()
    #
    # week = threading.Thread(target=week.care, args=(app.client, connection_pool, config, 5,))
    # week.start()
    #
    bot = threading.Thread(target=app.start(port=config["bot"]["port"]), args=())
    bot.start()
    #
    # pairs.join()
    # week.join()
    # bot.join()
