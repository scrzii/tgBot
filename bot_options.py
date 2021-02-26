from serializer_class import *


class Options:
    def __init__(self, timeout: int=None, check_interval: float=2,
                 serializer_tool: Serializer=None, serializer_path: str="../serialized_data/",
                 new_user_function=None, loop_function=None):
        serializer_path = smet(serializer_path)
        if not serializer_tool:
            serializer_tool = FileSerializer(serializer_path)
        self.timeout = timeout
        self.check_interval = check_interval
        self.serializer_tool = serializer_tool
        self.serializer_path = serializer_path
        self.new_user_function = new_user_function
        self.loop_function = loop_function
