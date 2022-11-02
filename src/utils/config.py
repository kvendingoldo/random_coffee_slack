# -*- coding: utf-8 -*-

import os
import environ
import time
import yaml

from datetime import date
from utils import groups


def load(yaml_path):
    with open(yaml_path, "r") as file:
        config = yaml.safe_load(file)

    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_app_token = os.environ.get("SLACK_APP_TOKEN")

    db_password = os.environ.get("DATABASE_PASSWORD")

    config["slack"] = {
        "botToken": slack_bot_token,
        "appToken": slack_app_token
    }

    config["database"]["password"] = db_password

    config["generated"] = {}
    config["generated"]["groups"] = groups.get_groups(config["bot"]["locations"], config["bot"]["groups"])

    return config


def get_week_info(config):
    if config["devMode"]["enabled"]:
        weekday = int(config["devMode"]["weekday"])
        hour = int(config["devMode"]["hour"])
    else:
        weekday = date.today().weekday() + 1
        hour = int(time.strftime("%H"))

    return weekday, hour
