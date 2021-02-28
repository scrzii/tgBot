from tg_api_worker import API, Keyboard
from tg_object_classes import User, Updater
from __init__ import TelegramBotCreator
from message_handler_abs import MessageHandlerAbs


class MessageHandler(MessageHandlerAbs):
    """
    Inherit from this class!!!
    """
    @staticmethod
    def handler(user: User, update: Updater.Update, bot_obj: TelegramBotCreator):
        pass

    @staticmethod
    def new_user(user: User, bot_obj: TelegramBotCreator):
        pass
