# -*- coding: utf-8 -*-

class User:
    def __init__(self, username, uid, loc="none", ready=True, pause_in_weeks=0):
        self.username = username
        self.uid = uid
        self.ready = ready
        self.pause_in_weeks = pause_in_weeks
        self.loc = loc
