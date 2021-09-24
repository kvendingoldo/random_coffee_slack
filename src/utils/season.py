# -*- coding: utf-8 -*-

from datetime import datetime, timedelta


def get(kind="current", days_delta=0):
    season = datetime.now()

    if kind == "next":
        season = season + timedelta(days=(7 - season.weekday()))
    elif kind == "previous":
        season = season - timedelta(days=(7 - season.weekday()))
    elif kind == "delta":
        season = season - timedelta(days=(days_delta - season.weekday()))

    return season.strftime("%Y%V")
