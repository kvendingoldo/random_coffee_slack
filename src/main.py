# -*- coding: utf-8 -*-

from slack_bolt import App
from loguru import logger
from mysql.connector import connect, Error
import threading
from algo import pair

sigSecret = "db26cd0745b8c2555ee77a42c16ee0c5"
otoken = "xoxb-1962766308593-1962780502497-JpOCNTLxOQWn6kbEJY91jb5b"

# Initializes your app with your bot token and signing secret
app = App(
    token=otoken,
    signing_secret=sigSecret,
)


@app.command("/wow")
def message(ack, say, command):
    ack()
    logger.info(
        f"Received /wow command from {command['user_name']} in {command['channel_name']} - {command['team_domain']}"
    )

    say("What's up?")


@app.action("action_start_join")
def action_start_join(body, ack, say):
    # Acknowledge the action
    ack(
        # redirect(url_for('message_onboard'))
    )

    say(
        text=f"Расскажи немного о себе",
        blocks=[],
        attachments=[
            {
                "fallback": "Upgrade your Slack client to use messages like these.",
                "color": "3AA3E3",
                "attachment_type": "default",
                "callback_id": "select_remote_1234",
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
        ]
    )


@app.message("start")
def message_start(message, say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Привет человек!👋\n" \
                            "Недавно я узнал о Random coffee challenge и понял - он нужен.\n" \
                            "Каждую неделю я буду предлагать тебе для встречи интересного человека, случайно выбранного среди других участников. " \
                            "Вы с ним увидите никнеймы друг друга и сможете сразу выбрать подходящий формат для встречи (в офисе, skype, zoom и т.д.).\n" \
                            "Интересно? Тогда присоединяйся!"
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://banner2.cleanpng.com/20180426/dww/kisspng-donuts-cafe-coffee-menu-donut-worry-pink-donut-5ae1808952de31.0211226315247279453394.jpg",
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
                        "action_id": "action_start_join",
                        "value": "click_me_123"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Help"
                        },
                        "action_id": "Help",
                        "value": "click_me_123"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Cancel"
                        },
                        "style": "danger",
                        "action_id": "cancel",
                        "value": "click_me_123"
                    }
                ]
            }
        ],
        text=f"Hello <@{message['user']}>!"
    )


def get_db():
    try:
        with connect(
                host="localhost",
                user="",
                password="",
        ) as connection:
            return connection
    except Error as e:
        print(e)


if __name__ == "__main__":
    connection = get_db()

    bot = threading.Thread(target=app.start, args=())
    bot.start()

    pairs = threading.Thread(target=pair.create, args=(60,))
    pairs.start()

    pairs.join()
    bot.join()
