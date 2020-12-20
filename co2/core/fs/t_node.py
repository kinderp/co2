from pprint import pprint

from .block import Block
from .dir_table import DirTable
from .types import Types

class TNode:
    def __init__(self, filename : str, block : Block=None, type:
                 str=Types.REGULAR, major : int=-1, minor : int=-1):
        self.__filename = filename
        self.__major_number = major
        self.__minor_number = minor
        self.__block_address = block
        if self.__block_address:
            self.__block_address.name = self.__filename
        self.__dir_table = DirTable()
        self.__type = type
        self.__is_mpoint = False
        self.__s_dev = None
    #def __repr__(self):
    #    print("filename={}".format(filename))
    #    print("type={}".format(self.__type))
    #    print("major_number={} minor_number={}".format(self.__major_number,self.__minor_number))
    #    print("block={}".format(self.__block_address))
    #    print("dir_table={}".format(self.__dir_table))

    @property
    def s_dev(self) -> str:
        return self.__s_dev

    @s_dev.setter
    def s_dev(self, s_dev : str):
        self.__s_dev = s_dev

    @property
    def is_mount_point(self) -> bool:
        return self.__is_mpoint

    @is_mount_point.setter
    def is_mount_point(self, is_mpoint : bool):
        self.__is_mpoint = is_mpoint

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
        return self.__type

    @property
    def major(self):
        return self.__major_number

    @property
    def minor(self):
        return self.__minor_number

    def add_dir_entry(self, t_node_number : int, filename : str):
        self.__dir_table._add(t_node_number, filename)

    def rem_dir_entry(self, filename: str) -> int:
        return self.__dir_table._rem(filename)

    def get_dir_entry(self, filename: str) -> int:
        return self.__dir_table._get(filename)
