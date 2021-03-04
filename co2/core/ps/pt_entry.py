class FDBitmap:
    RESERVED_FDS = (0, 1, 2)
    def __init__(self):
        self.bitmap = {
            0: True,
            1: True,
            2: True,
        }

    def _add(self, fd : int):
        self.bitmap[fd] = True

    def _rem(self, fd : int) -> int:
        return self.bitmap.pop(fd, None)

    def _get(self) -> int:
        max_fd = max(self.bitmap.keys())
        # start from 3 because 0,1,2 are reserved to:
        # - stdin
        # - stdout
        # - stderr
        #and can't used
        for fd_number in range(3, max_fd + 1):
            if not self.bitmap.get(fd_number, None):
                return fd_number
        return max_fd + 1


class FDTable:
    def __init__(self):
        self.bitmap = FDBitmap()
        self.table = {}

    def get(self, fd : int):
        return self.table[fd]

    def add(self, ftable_index : int) -> int:
        fd = self.reserve_fd()
        self.table[fd] = ftable_index
        return fd

    def rem(self, fd : int) -> bool:
        try:
            del self.table[fd]
        except  Exception as e:
            return False
        self.release_fd(fd)
        return True

    def reserve_fd(self) -> int :
        reserved = self.bitmap._get()
        self.bitmap._add(reserved)
        return reserved

    def release_fd(self, fd : int) -> int:
        return self.bitmap._rem(fd)


class PTEntry:
    def __init__(self):
        self.PID = None
        self.PPID = None
        self.FDTABLE = FDTable()
        self.__PWD = None
        """
        self.FDS = {

            0: None,
            1: None,
            2: None,
        }
        """

    @property
    def PWD(self):
        return self.__PWD

    @PWD.setter
    def PWD(self, PWD):
        splitted_pwd = PWD.split("/")
        path = []
        for elem in splitted_pwd:
            if elem == "..":
                path.pop()
            elif elem == ".":
                continue
            else:
                path.append(elem)
        pwd = '/'.join(path)
        self.__PWD = pwd if pwd else "/"




