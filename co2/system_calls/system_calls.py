from co2.core.fs import Fs
from co2.core.fs import Types as FilesTypes
from co2.core.fs import OFlags

class IOSystemCalls:

    fs = Fs()

    @classmethod
    def open(cls, abs_filename : str, oflags : OFlags):
        return cls.fs.do_open(abs_filename, oflags, FilesTypes.REGULAR)

    @classmethod
    def unlink(cls, abs_filename : str):
        return cls.fs.do_unlink(abs_filename)

    @classmethod
    def mkdir(cls, abs_filename : str):
       return cls.fs.do_mkdir(abs_filename, FilesTypes.DIRECTORY)

    @classmethod
    def rmdir(cls, abs_filename : str):
       return cls.fs.do_rmdir(abs_filename)
