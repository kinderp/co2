from pprint import pprint

class TNodesBitmap:

    bitmap = {0:True}

    def __repr__(self):
        pprint(self.bitmap)
        return super().__repr__()

    @classmethod
    def _add(cls, t_node_number : int):
        cls.bitmap[t_node_number] = True

    @classmethod
    def _rem(cls, t_node_number : int) -> int:
        return cls.bitmap.pop(t_node_number, None)

    @classmethod
    def _get(cls) -> int:
        max_t_node_number = max(cls.bitmap.keys())
        # start from 1 because 0 is reserved to / and can't used
        for t_node_number in range(1, max_t_node_number + 1):
            if not cls.bitmap.get(t_node_number, None):
                return t_node_number
        return max_t_node_number + 1

