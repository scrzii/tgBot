from tg_api_worker import *


class Updater:
    class Message:
        pass

    class CallbackQuery:
        pass


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
        def default(user, message):  # Default handler. You should override this
            user.send("Вы написали сообщение")

    class Callbacks:
        """
        This class handles user's button callbacks (InlineKeyboard - look at tg api documentation)
        Override default and add other methods
        """
        @staticmethod
        def default(user, callback):  # Default handler. You should override this
            user.send("Вы нажали коллбэк-кнопку")
