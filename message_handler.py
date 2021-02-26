from tg_api_worker import *
from tg_object_classes import *


class MessageHandler:
    """
    Inherit from this class!!!
    """
    class Messages:
        """
        This class handles user's messages
        Override default and add other methods
        """
        @staticmethod
        def default(self, user: User, message: Updater.Message):  # Default handler. You should override this
            user.send("Вы написали сообщение")

    class Callbacks:
        """
        This class handles user's button callbacks (InlineKeyboard - look at tg api documentation)
        Override default and add other methods
        """
        @staticmethod
        def default(self, user: User, callback: Updater.CallbackQuery):  # Default handler. You should override this
            user.send("Вы нажали коллбэк-кнопку")
