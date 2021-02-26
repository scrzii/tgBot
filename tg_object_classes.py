from tg_api_worker import *
from message_handler import *


class Updater:
    class Update:
        def __init__(self, source: dict):
            """
            Initializing fields for update
            :param source: dict source
            """
            self.source = source
            self.update_id = int(source["update_id"])
            self.chat_id = int(source["chat"]["id"])

        def __getitem__(self, item):
            return self.source[item]

    class Message(Update):
        """
        User's message
        """
        def __init__(self, source: dict):
            super().__init__(source)
            self.message_source = source["message"]
            self.message_id = self.message_source["message_id"]
            self.text = ""
            if "text" in self.message_source:
                self.text = self.message_source["text"]

    class CallbackQuery(Update):
        """
        When user presses on inline button, callback query occurs
        """
        def __init__(self, source: dict):
            super().__init__(source)
            self.callback_source = source["callback_query"]
            self.id = callback_source["id"]

    class UndefinedUpdate(Update):
        """
        In case I did not take into account some option
        Think about it and FIXME
        """
        def __init__(self, source: dict):
            super().__init__(source)

    @staticmethod
    def auto_distribute(source: dict) -> Updater.Update:
        if "callback_query" in source:
            return Updater.CallbackQuery(source)
        elif "message" in source:
            return Updater.Message(source)
        return Updater.UndefinedUpdate(source)


class User:
    def __init__(self, api: API, source: dict, current_message: str="", local_data=None, initializer: function=None):
        self.api = api
        self.source = source  # Info about user from telegram api request
        self.current_message = current_message  # Last user's message
        self.local_data = local_data if local_data else {}  # Local data for this user in your project
        self.id = source["id"]
        self.cc_handler = cc_handler if cc_handler else MessageHandler.Callbacks.default  # Current callback handler
        self.cm_handler = cm_handler if cm_handler else MessageHandler.Messages.default  # Current message handler
        if initializer:
            initializer(self)

    def update_text(self, text):
        self.current_message = text

    def send(self, text: str, keyboard: Keyboard=None):
        if keyboard:
            self.api.send_message(chat_id=self.id, text=text, reply_markup=str(keyboard))
        else:
            self.api.send_message(chat_id=self.id, text=text)

    def get(self):
        return self.current_message

    def __str__(self):
        return self.get()
