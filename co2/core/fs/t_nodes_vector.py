from .t_node import TNode
from .block import Block
from .types import Types

class TNodesVector:
    vector = {
                0: TNode(filename="/", block=Block(name="/", children=[]), type=Types.DIRECTORY)
    }

    @classmethod
    def add_entry(cls, vector_entry : TNode, vector_entry_index : int):
        cls.vector[vector_entry_index] = vector_entry

    @classmethod
    def rem_entry(cls, vector_entry_index : int) -> TNode:
        return cls.vector.pop(vector_entry_index, None)

    @classmethod
    def get_entry(cls, vector_entry_index : int) -> TNode:
        return cls.vector.get(vector_entry_index, None)
