from .t_nodes_bitmap import TNodesBitmap
from .t_nodes_vector import TNodesVector

class Superblock:

    bitmap = TNodesBitmap()
    vector = TNodesVector()

    @classmethod
    def reserve_t_node_number(cls) -> int :
        reserved = cls.bitmap._get()
        cls.bitmap._add(reserved)
        return reserved

    @classmethod
    def release_t_node_number(cls, t_node_number : int) -> int:
        return cls.bitmap._rem(t_node_number)
