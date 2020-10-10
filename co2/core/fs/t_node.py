from .block import Block
from .dir_table import DirTable
from .types import Types

class TNode:
    def __init__(self, filename : str, block : Block=None, type: str=Types.REGULAR):
        self.__filename = filename
        self.__major_number = -1
        self.__minor_number = -1
        self.__block_address = block
        if self.__block_address:
            self.__block_address = self.__filename
        self.__dir_table = DirTable()
        self.__type = type

    @property
    def filename(self) -> str:
        return self.__filename

    @property
    def block(self):
        return self.__block_address

    @block.setter
    def block(self, block: Block):
        self.__block_address = block

    @property
    def dir_table(self):
        return self.__dir_table.table

    @property
    def type(self):
        return self.type

    def add_dir_entry(self, t_node_number : int, filename : str):
        self.__dir_table._add(t_node_number, filename)

    def rem_dir_entry(self, filename: str) -> int:
        return self.__dir_table._rem(filename)

    def get_dir_entry(self, filename: str) -> int:
        return self.__dir_table._get(filename)
