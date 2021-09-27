# -*- coding: utf-8 -*-
import re


def get_ts(body):
    if "original_message" in body.keys():
        ts = body["original_message"]["ts"]
    else:
        ts = body["message"]["ts"]

    return ts


def get_uid(text):
    uid = re.sub("<@|>", "", re.findall(r'(<@.*>)', text)[0])

    return uid
