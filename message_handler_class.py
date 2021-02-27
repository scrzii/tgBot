from tg_api_worker import *
from tg_object_classes import *


class MessageHandler:
    """
    Inherit from this class!!!
    """
    @staticmethod
    def handler(user, update):
        pass

    @staticmethod
    def new_user(user):
        pass
