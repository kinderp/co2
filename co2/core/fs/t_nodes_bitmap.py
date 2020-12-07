from pprint import pprint

class TNodesBitmap:

    def __init__(self):
        self.bitmap = {0:True}

    def __repr__(self):
        pprint(self.bitmap)
        return super().__repr__()

    def _add(self, t_node_number : int):
        self.bitmap[t_node_number] = True

    def _rem(self, t_node_number : int) -> int:
        return self.bitmap.pop(t_node_number, None)

    def _get(self) -> int:
        max_t_node_number = max(self.bitmap.keys())
        # start from 1 because 0 is reserved to / and can't used
        for t_node_number in range(1, max_t_node_number + 1):
            if not self.bitmap.get(t_node_number, None):
                return t_node_number
        return max_t_node_number + 1

