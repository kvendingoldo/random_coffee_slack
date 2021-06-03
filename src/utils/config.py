# -*- coding: utf-8 -*-

import yaml
import os
from dotenv import load_dotenv


def load(yaml_path, env_path):
    with open(yaml_path, "r") as f:
        config = yaml.safe_load(f)

    load_dotenv(env_path)

    slack_otoken = os.environ.get("SLACK_OTOKEN")
    slack_sigsecret = os.environ.get("SLACK_SIGSECRET")
    db_password = os.environ.get("DATABASE_PASSWORD")

    config["slack"] = {
        "otoken": slack_otoken,
        "sigSecret": slack_sigsecret
    }

    config["database"]["password"] = db_password

    print(config)

    return config
