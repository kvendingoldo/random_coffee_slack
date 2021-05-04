# -*- coding: utf-8 -*-

import time

from database.dao import users
from database.interface import connector
from datetime import date


def meet_reminder(sclient, user):
    # TODO: check if meeting hasn't been done
    completed = False

    if not completed:
        # TODO: get partner name
        sclient.chat_postMessage(channel=user.uid,
                                 text="✉️ How are things?\n\n" \
                                      "Meed-week is the best day to set up a meeting with your coffee partner!\n\n" \
                                      "Slack them now to set up a meeting."
                                 )

    def ask_about_meet(sclient, user):
        sclient.chat_postMessage(channel=user.uid,
                                 text="",

                                 # TODO: GET NAME

                                 blocks=[
                                     {
                                         "type": "section",
                                         "text": {
                                             "type": "mrkdwn",
                                             "text": "The week is over!" \
                                                     "Did you get a chance to catch up with @nickname for a coffee break?"
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
                                                     "text": "Yes"
                                                 },
                                                 "style": "primary",
                                                 "action_id": "flow_meet_was"
                                             },
                                             {
                                                 "type": "button",
                                                 "text": {
                                                     "type": "plain_text",
                                                     "emoji": True,
                                                     "text": "No"
                                                 },
                                                 "style": "danger",
                                                 "action_id": "flow_meet_was_not"
                                             }
                                         ]
                                     }
                                 ]
                                 )
        # TODO: do smth with rating

    def ask_about_next_week(sclient, user):
        sclient.chat_postMessage(channel=user.uid,
                                 text="",
                                 blocks=[
                                     {
                                         "type": "section",
                                         "text": {

                                             "type": "mrkdwn",
                                             "text": "New week – new opportunities!\n\n" \
                                                     "Are you taking part in Random Coffee meetings next week?"

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
                                                     "text": "Sure!"
                                                 },
                                                 "style": "primary",
                                                 "action_id": "flow_next_week_yes"
                                             },
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
                                                 "action_id": "flow_stop"
                                             }
                                         ]
                                     }
                                 ]
                                 )

    def care(slack_client, connection_pool, period):
        connector = connector.Connector(connection_pool)

        while True:
            for user in users.list(connector):
                cur_day = date.today().weekday()

                if cur_day == 2:
                    meet_reminder(slack_client, user)

                if cur_day == 4:
                    ask_about_next_week(slack_client, user)
                    ask_about_meet(slack_client, user)

            time.sleep(period)
