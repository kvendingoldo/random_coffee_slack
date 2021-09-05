# -*- coding: utf-8 -*-


def get_ts(body):
    if "original_message" in body.keys():
        ts = body["original_message"]["ts"]
    else:
        ts = body["message"]["ts"]

    return ts
