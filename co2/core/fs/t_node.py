from pprint import pprint

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
            self.__block_address.name = self.__filename
        self.__dir_table = DirTable()
        self.__type = type

    #def __repr__(self):
    #    print("filename={}".format(filename))
    #    print("type={}".format(self.__type))
    #    print("major_number={} minor_number={}".format(self.__major_number,self.__minor_number))
    #    print("block={}".format(self.__block_address))
    #    print("dir_table={}".format(self.__dir_table))

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
        return self.__dir_table

    @property
    def type(self):
        return self.type

    def add_dir_entry(self, t_node_number : int, filename : str):
        self.__dir_table._add(t_node_number, filename)

    def rem_dir_entry(self, filename: str) -> int:
        return self.__dir_table._rem(filename)

    def get_dir_entry(self, filename: str) -> int:
        return self.__dir_table._get(filename)
