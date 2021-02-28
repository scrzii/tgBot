from tg_api_worker import API, Keyboard
from message_handler_abs import MessageHandlerAbs


class Updater:
    class Update:
        def __init__(self, source: dict):
            """
            Initializing fields for update
            :param source: dict source
            """
            self.source = source
            self.update_id = int(source["update_id"])

        def __getitem__(self, item):
            return self.source[item]

    class Message(Update):
        """
        User's message
        """
        def __init__(self, source: dict):
            super().__init__(source)
            self.inner_source = source["message"]
            self.message_id = self.inner_source["message_id"]
            self.text = ""
            if "text" in self.inner_source:
                self.text = self.inner_source["text"]

    class CallbackQuery(Update):
        """
        When user presses on inline button, callback query occurs
        """
        def __init__(self, source: dict):
            super().__init__(source)
            self.inner_source = source["callback_query"]
            self.id = inner_source["id"]

    class UndefinedUpdate(Update):
        """
        In case I did not take into account some option
        Think about it and FIXME
        """
        def __init__(self, source: dict):
            super().__init__(source)
            self.inner_source = {}

    @staticmethod
    def auto_distribute(source: dict) -> Update:
        if "callback_query" in source:
            return Updater.CallbackQuery(source)
        elif "message" in source:
            return Updater.Message(source)
        return Updater.UndefinedUpdate(source)


class User:
    def __init__(self, api: API, source: dict, message_handler: type, current_message: str="", data=None):
        self.api = api
        self.source = source  # Info about user from telegram api request
        self.current_message = current_message  # Last user's message
        self.data = data if data else {}  # Local data for this user in your project
        self.id = source["id"]
        self.message_handler = message_handler

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
