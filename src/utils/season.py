# -*- coding: utf-8 -*-

from datetime import datetime, timedelta


def get_current():
    season = datetime.now().strftime("%Y%V")
    return season


def get_next():
    today = datetime.now()
    season = (today + timedelta(days=(7 - today.weekday()))).strftime("%Y%V")
    return season
