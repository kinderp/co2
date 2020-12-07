from .t_node import TNode
from .block import Block
from .types import Types

class TNodesVector:
    def __init__(self):
        self.vector = {
                0: TNode(filename="/", block=Block(name="/", children=[]), type=Types.DIRECTORY)
        }

    def add_entry(self, vector_entry : TNode, vector_entry_index : int):
        self.vector[vector_entry_index] = vector_entry

    def rem_entry(self, vector_entry_index : int) -> TNode:
        return self.vector.pop(vector_entry_index, None)

    def get_entry(self, vector_entry_index : int) -> TNode:
        return self.vector.get(vector_entry_index, None)
