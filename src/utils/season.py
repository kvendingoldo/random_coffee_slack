# -*- coding: utf-8 -*-

from datetime import datetime


def get_current():
    season = datetime.now().strftime("%Y%V")
    return season


def get_next():
    season = datetime.now().strftime("%Y%V")
    return season
