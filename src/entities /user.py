# -*- coding: utf-8 -*-

class User(object):
    def __init__(self, uid, username,
                 ready=False, be_notified=False):
        self.uid = uid
        self.username = username
        self.ready = ready
        self.be_notified = be_notified
