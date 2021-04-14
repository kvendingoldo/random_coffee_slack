# -*- coding: utf-8 -*-

from slack_bolt import App
from loguru import logger

sigSecret = ""
otoken = ""

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
    say(command["text"])


# Start your app
if __name__ == "__main__":
    app.start(port=80)
