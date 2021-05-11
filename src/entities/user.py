# -*- coding: utf-8 -*-

class User:
    def __init__(self, username, uid, loc="none", ready=False, aware=False):
        self.username = username
        self.uid = uid
        self.ready = ready
        self.aware = aware
        self.loc = loc
