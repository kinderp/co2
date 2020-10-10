from .t_nodes_bitmap import TNodesBitmap
from .t_nodes_vector import TNodesVector

class Superblock:
    def __init__(self):
        self.__t_nodes_bitmap = TNodesBitmap()
        self.__t_nodes_vector = TNodesVector()

    @property
    def bitmap(self):
        return self.__t_nodes_bitmap

    @property
    def vector(self):
        return self.__t_nodes_vector

    def reserve_t_node_number(self) -> int :
        reserved = self.__t_nodes_bitmap._get()
        self.__t_nodes_bitmap._add(reserved)
        return reserved

    def release_t_node_number(self, t_node_number : int) -> int:
        return self.__t_nodes_bitmap._rem(t_node_number)
