from ..elf import Elf

from co2.co2lib.fcntl import open
from co2.co2lib.unistd import write
from co2.core.fs.fs import OFlags


class VPC(Elf):
    MAGIC_NUMBER = 100
    def text(self):
        # Analisi semantica
        # TODO       

        # 1 controllare che il padre abbia un tipo e che sia compatibile con il
        # mio

        # 2. controllare se i figli hanno già un tipo e che siano compatibili con
        # il mio
        fd = open("/dev/vpc", OFlags.O_WRONLY)
        write(fd, ["BUILD"], 1)
