from .pt_entry import PTEntry


class PTable:

    # start from 1 (init)
    # 0 is reserved for swapper process
    #PTABLE_INDEX = 1

    def __init__(self):
        self.table = {}

    def add_entry(self, pid :str, pt_entry : PTEntry) -> bool:
        try:
            #self.table[self.PTABLE_INDEX] = pt_entry
            #current_index = self.PTABLE_INDEX
            #self.PTABLE_INDEX += 1
            self.table[pid] = pt_entry
            return True
        except Exception as e:
            return False

    def rem_entry(self, pid : str) -> bool:
        try:
            del self.table[pid]
            return True
        except Exception as e:
            return False

    def get_entry(self, pid : str):
        return self.table.get(pid)
