# -*- coding: utf-8 -*-

class User(object):
    def __init__(self, username, uid, loc="none", ready=False, aware=False):
        self.username = username
        self.uid = uid
        self.ready = ready
        self.aware = aware
        self.loc = loc

    # @property
    # def name(self):
    #     return self.name
    #
    # @name.setter
    # def name(self, value):
    #     self._name = value
    #
    # @property
    # def username(self):
    #     return self.username
    #
    # @username.setter
    # def username(self, value):
    #     self.username = value
    #
    # @property
    # def channel_id(self):
    #     return self.channel_id
    #
    # @channel_id.setter
    # def channel_id(self, value):
    #     self.channel_id = value
    #
    # @property
    # def ready(self):
    #     return self.readys
    #
    # @ready.setter
    # def ready(self, value):
    #     self.ready = value
    #
    # @property
    # def aware(self):
    #     return self.aware
    #
    # @aware.setter
    # def aware(self, value):
    #     self.aware = value
