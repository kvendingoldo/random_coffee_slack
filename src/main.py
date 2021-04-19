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
def flow_0_start(message, say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    # TODO (asharov): rewrite
                    "type": "mrkdwn",
                    "text": "Привет человек (текст будет переписан!)👋 \n" \
                            "Недавно я узнал о Random coffee challenge и понял - он нужен.\n" \
                            "Каждую неделю я буду предлагать тебе для встречи интересного человека, случайно выбранного среди других участников." \
                            "Вы с ним увидите никнеймы друг друга и сможете сразу выбрать подходящий формат для встречи (в офисе, skype, zoom и т.д.).\n" \
                            "Интересно? Тогда присоединяйся!"
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
                        "action_id": "flow_1_start"
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
                        "action_id": "flow_0_cancel"
                    }
                ]
            }
        ],
        text=""
    )

@app.action("location")
def location(body, ack, say):
    logger.info("location :::", body)
    uuser = user.User(username=body["user"]["name"],
                      uid=body["user"]["id"],
                      loc=body["actions"][0]["selected_options"][0]["value"])
    usersDAO.set_loc(uuser)

@app.action("flow_1_start")
def flow_1_start(body, ack, say):
    uuser = user.User(username=body["user"]["username"], uid=body["user"]["id"])
    uuuser = usersDAO.get_user(body["user"]["id"])
    if not uuuser or uuuser.loc == "none":
        usersDAO.add(uuser)

        ack()
        say(
            text=f"Расскажи немного о себе",
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
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": "Done"
                            },
                            "style": "primary",
                            "action_id": "flow_2_start",
                            "value": "click_me_123"
                        }
                    ]
                }

            ]
        )
    else:
        flow_2_start(body, ack, say)


@app.action("flow_0_cancel")
def flow_1_cancel(body, ack, say):
    ack()
    logger.info("flow_0_cancel :::", body)
    say(
        text=f"TODO: flow_0_cancel"
    )


@app.action("flow_2_start")
def flow_2_start(body, ack, say):
    logger.info("flow_2_start :::", body)
    uuser = usersDAO.get_user(uid=body["user"]["id"])
    if uuser.loc == "none":
        flow_1_start(body, ack, say)
    else:
        ack()
        say(
            text=f"TODO: flow_help"
        )


@app.action("flow_next_week_yes")
def flow_next_week_yes(body, ack, say):
    ack()
    say(
        text=f"Отлично!👍! Напишу тебе в понедельник."
    )

    # user.ready = True
    # users.set_ready(connection, user)


@app.action("flow_next_week_no")
def flow_next_week_no(body, ack, say):
    ack()
    say(
        text=f"Перерыв нужен всегда, понимаю. Вернусь к тебе на следующей неделе"
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
