# -*- coding: utf-8 -*-

class NoResultFound(Exception):
    def __init__(self, message="No SQL result found"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
