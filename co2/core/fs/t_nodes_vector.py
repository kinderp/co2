from .t_node import TNode

class TNodesVector:
    vector = {}

    @classmethod
    def add_entry(cls, vector_entry : TNode, vector_entry_index : int):
        cls.vector[vector_entry_index] = vector_entry

    @classmethod
    def rem_entry(cls, vector_entry_index : int) -> TNode:
        return cls.vector.pop(vector_entry_index, None)

    @classmethod
    def get_entry(cls, vector_entry_index : int) -> TNode:
        return cls.vector.get(vector_entry_index, None)
