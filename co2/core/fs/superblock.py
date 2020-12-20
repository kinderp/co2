from .t_nodes_bitmap import TNodesBitmap
from .t_nodes_vector import TNodesVector

class Superblock:

    def __init__(self, s_dev=None, s_imount=None):
        self.s_imount = s_imount  # tnode mounted on
        self.s_dev    = s_dev     # block device id for current superblock
        self.bitmap   = TNodesBitmap()
        self.vector   = TNodesVector()
        self.s_isup   = self.vector.get_entry(0)    # tnode for root dir of mounted fs

    def reserve_t_node_number(self) -> int :
        reserved = self.bitmap._get()
        self.bitmap._add(reserved)
        return reserved

    def release_t_node_number(self, t_node_number : int) -> int:
        return self.bitmap._rem(t_node_number)
