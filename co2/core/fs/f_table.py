class FTable:
    INDEX = 0
    def __init__(self):
        self.ftable = {}
        self.count = {}
        self.s_dev = {}

    def get_entry(self, ftable_index : int)-> int:
        return self.ftable.get(ftable_index), self.count.get(ftable_index), self.s_dev.get(ftable_index)

    def add_entry(self, t_node_number : int, s_dev : str = "ram0") -> int:
        i = self.INDEX
        self.ftable[i] = t_node_number
        self.count[i] = 1
        self.s_dev[i] = s_dev
        self.INDEX +=1
        return i

    def del_entry(self, index) -> int:
        if self.count[index] == 1:
            try:
                del self.ftable[index]
                del self.count[index]
                del self.s_dev[index]
                return 1
            except Exception as e:
                return -1
        elif self.count[index] > 1:
            self.count[index] -= 1
            return 1
        else: # zero
            return -1


