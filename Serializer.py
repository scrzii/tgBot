import pickle


class Serializer:
    """
    Class for serializing all object or simple field of object
    """

    def __init__(self):  # Override me
        pass

    def export_to(self, field: str, value: object):  # Override me
        pass

    def import_from(self, field: str) -> object:  # Override me
        pass


class FileSerializer(Serializer):
    """
    This class realizes file serializing with Pickle
    Each object is stored in simple .pickle-file
    """
    def __init__(self, file_path: str):
        """
        All files must be in one directory (file_path)
        :param file_path:
        """
        super().__init__()
        if not file_path.endswith("/"):
            file_path += "/"
        self.file_path = file_path

    def export_to(self, field: str, value: object):
        if not field.endswith(".pickle"):
            field += ".pickle"
        pickle.dump(data, open(self.file_path + field, "wb"))

    def import_from(self, field: str):
        if not field.endswith(".pickle"):
            field += ".pickle"
        return pickle.load(open(self.file_path + field, "rb"))
