from serializer import *


class Options:
    def __init__(self, timeout: int=None, check_interval: float=2,
                 serializer_tool: Serializer=None, serializer_path: str="./"):
        serializer_path = smet(serializer_path)
        if not serializer_tool:
            serializer_tool = FileSerializer(serializer_path)
        self.timeout = timeout
        self.check_interval = check_interval
        self.serializer_tool = serializer_tool
        self.serializer_path = serializer_path
