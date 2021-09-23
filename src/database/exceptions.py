# -*- coding: utf-8 -*-

class NoResultFound(Exception):
    def __init__(self, message="No SQL result found"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f'{self.entity_name} not found, id: {entity_id}')


class MeetNotFoundError(NotFoundError):
    entity_name: str = 'Meet'


class NotificationNotFoundError(NotFoundError):
    entity_name: str = 'Notification'


class UserNotFoundError(NotFoundError):
    entity_name: str = 'User'
