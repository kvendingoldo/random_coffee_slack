# -*- coding: utf-8 -*-

class User(object):
    def __init__(self, username, name, channel_id, ready=False, aware=False):
        self.username = username
        self.name = name
        self.channel_id = channel_id
        self.ready = ready
        self.aware = aware

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def username(self):
        return self.username

    @username.setter
    def username(self, value):
        self.username = value

    @property
    def channel_id(self):
        return self.channel_id

    @channel_id.setter
    def channel_id(self, value):
        self.channel_id = value

    @property
    def ready(self):
        return self.ready

    @ready.setter
    def ready(self, value):
        self.ready = value

    @property
    def aware(self):
        return self.aware

    @aware.setter
    def aware(self, value):
        self.aware = value
