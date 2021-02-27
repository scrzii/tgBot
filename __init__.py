import json
import time

from tg_api_worker import *
from extensions import *
from tg_object_classes import *
from bot_options import *
from serializer_class import *


class TelegramBotCreator:
    def __init__(self, access_token: str, message_handler: type, options: Options=None):
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
                if "from" in update.inner_source:  # We know who sent this update
                    # (updates in channels may be without sender)

                    # Handle if we know update's user only
                    user_source = update.inner_source["from"]
                    user_id = str(user_source["id"])
                    need_update.add(user_id)

                    if user_id not in self.users:  # This member is not in RAM
                        if serializer.field_exists(user_id):  # User is in serialized data
                            user_data = serializer.import_from(user_id)
                            user = User(api, user_source, self.message_handler, data=user_data, new=False)
                        else:  # This is a new user
                            user = User(api, user_source, self.message_handler)  # Creating new user

                        self.users[user_id] = user  # Adding new user to RAM

                    user = self.users[user_id]
                    if type(update) == Updater.Message:  # If type of update is message
                        user.update_text(update.text)  # Text of user's message

                    user.message_handler.handle(user, update)

                offset = int(update.update_id) + 1  # Updating offset for removing old updates (look at tg api)
            for user_id in need_update:
                user = self.users[user_id]
                serializer.export_to(user_id, user.data)
            time.sleep(self.options.check_interval)  # Wait before next check


def main():
    class MyMessageHandler(MessageHandler):
        @staticmethod
        def handle(user: User, update: Updater.Update):
            user.send(f"Вы написали: {user.current_message}. Ваш stage: {user.data['stage']}")

        @staticmethod
        def new_user(user):
            user.data["stage"] = "default"

    access_token = "ACCESS_TOKEN"
    bot = TelegramBotCreator(access_token, MyMessageHandler)
    bot.mainloop()


if __name__ == "__main__":
    main()
