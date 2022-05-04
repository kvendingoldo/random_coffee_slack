# -*- coding: utf-8 -*-

import datetime


def get_current_hour(offset):
    """
    :param offset: seconds
    :return: current hour in 24h format
    """
    now = datetime.datetime.utcnow() + datetime.timedelta(seconds=offset)
    return int(now.strftime("%H"))


def get_current_time(offset):
    """
    :param offset: seconds
    :return: current hour in 24h format
    """
    now = datetime.datetime.utcnow() + datetime.timedelta(seconds=offset)
    return now.strftime("%m-%d %H:%m:%S")
