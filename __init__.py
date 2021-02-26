import json
import time

from tg_api_worker import *
from serializer_class import *
from extensions import *
from tg_object_classes import *
from message_handler_class import *
from bot_options import *


class TelegramBotCreator:
    def __init__(self, access_token: str, message_handler: MessageHandler, options: Options=None):
        self.access_token = access_token
        self.message_handler = message_handler
        if not options:
            options = Options()
        self.options = options
        self.users = {}  # Don't store unnecessary users in RAM. Store them in updating process

    def mainloop(self):
        time_started = time.time()
        api = API(self.access_token)
        serializer = self.options.serializer_tool
        offset = 0
        while True:
            current_time = time.time()
            timeout = self.options.timeout
            if timeout and current_time - time_started >= timeout:  # Checking timeout and breaking loop
                break

            updates_raw = api.get_updates(offset=offset)["result"]  # Getting updates in dict format
            updates = list(map(Updater.auto_distribute, updates_raw))  # Getting updates in Update-class format
            need_update = set()  # User ids which we must update with serializer
            for update in updates:
                if "from" in update.source:  # We know who sent this update (updates in channels may be without sender)

                    # Handle if we know update's user only
                    user_source = update.source["from"]
                    user_id = str(user_source["id"])
                    need_update.add(user_id)

                    if user_id not in self.users:  # This member is not in RAM
                        if serializer.field_exists(user_id):  # User is in serialized data
                            user = serializer.import_from(user_id)
                        else:  # This is a new user
                            user = User(api, user_source, self.message_handler,
                                        initializer=self.options.new_user_function)  # Creating new user
                            if type(update) == MessageHandler.Messages:  # If type of update is message
                                user.current_message = update.text  # Text of user's message
                        self.users[user_id] = user  # Adding new user to RAM

                    user = self.users[user_id]
                    if type(update) == Updater.Message:
                        user.cm_handler(user, update)
                    elif type(update) == Updater.CallbackQuery:
                        user.cc_handler(user, update)

                offset = int(update.update_id) + 1  # Updating offset for removing old updates (look at tg api)
            for user_id in need_update:
                serializer.export_to(user_id, self.users[user_id])
            time.sleep(self.options.check_interval)  # Wait before next check


def main():
    print(dir(Updater))
    class MyMessageHandler(MessageHandler):
        class MyMessages(MessageHandler.Messages):
            @staticmethod
            def default(user: User, message: Updater.Message):
                user.send(f"Вы написали: {str(user)}")
                user.cm_handler = default

        class MyCallbacks(MessageHandler.Callbacks):
            @staticmethod
            def default(user: User, callback: Updater.CallbackQuery):
                pass

    message_handler = MyMessageHandler()
    access_token = "1676592005:AAHSZM0-_iTGa3Qeoz8ZNGgaCQiaBMzUYzY"
    bot = TelegramBotCreator(access_token, message_handler)
    bot.mainloop()


if __name__ == "__main__":
    main()
