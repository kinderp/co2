class Block:
    def __init__(self, type : str = None, data : object = None):
        self.__type = type
        self.__data = data

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data: object):
        self.__data = data

    @property
    def type(self):
        return self.__type

