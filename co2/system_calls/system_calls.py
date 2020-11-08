from co2.core.fs import Fs
from co2.core.fs import Types as FilesTypes
from co2.core.fs import OFlags

class IOSystemCalls:

    fs = Fs()

    @classmethod
    def init(cls):
        cls.mkdir("/dev")
        cls.mknod("/dev/hda", 1, 2)
        cls.mknod("/dev/console", 3, 4)

    @classmethod
    def open(cls, abs_filename : str, oflags : OFlags):
        return cls.fs.do_open(abs_filename, oflags, FilesTypes.REGULAR)

    @classmethod
    def unlink(cls, abs_filename : str):
        return cls.fs.do_unlink(abs_filename)

    @classmethod
    def mkdir(cls, abs_filename : str):
        return cls.fs.do_mkdir(abs_filename, OFlags.O_WRONLY | OFlags.O_CREAT)

    @classmethod
    def rmdir(cls, abs_filename : str):
        return cls.fs.do_rmdir(abs_filename)

    @classmethod
    def mknod(cls, abs_filename : str, major : int, minor : int):
        return cls.fs.do_mknod(abs_filename, major, minor)
