class DirTable:
    def __init__(self):
        self.__table = {}

    @property
    def table(self):
        return self.__table

    def _add(self, t_node_number : int, filename : str):
        self.__table[filename] = t_node_number

    def _rem(self, filename : str) -> int:
        return self.__table.pop(filename, None)

    def _get(self, filename : str) -> int :
        return self.__table.get(filename, None)
