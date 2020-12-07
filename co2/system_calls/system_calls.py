from pathlib import Path
import shelve

from co2.core.fs import Fs
from co2.core.fs import Types as FilesTypes
from co2.core.fs import OFlags

class IOSystemCalls:

    super_table = {
        'ram0': Fs(s_dev='ram0', s_isup=None, s_imount=None)
    }

    @classmethod
    def init(cls):
        import pdb
        pdb.set_trace()

        Path(".co2/objects").mkdir(parents=True, exist_ok=True)
        db = shelve.open(".co2/objects/co2")
        if 'ram0' in db:
            cls.super_table['ram0'] = db['ram0']
        else:
            cls.mkdir("/dev", dev_t='ram0')
            #cls.mknod("/dev/hda", 1, 2, dev_t='ram0')
            #cls.mknod("/dev/console", 3, 4, dev_t='ram0')

    @classmethod
    def open(cls, abs_filename : str, oflags : OFlags, dev_t : str = 'ram0'):
        return cls.super_table.get(dev_t).do_open(abs_filename, oflags, FilesTypes.REGULAR)

    @classmethod
    def unlink(cls, abs_filename : str, dev_t : str = 'ram0'):
        return cls.super_table.get(dev_t).do_unlink(abs_filename)

    @classmethod
    def mkdir(cls, abs_filename : str, dev_t : str = 'ram0'):
        return cls.super_table.get(dev_t).do_mkdir(abs_filename, OFlags.O_WRONLY | OFlags.O_CREAT)

    @classmethod
    def rmdir(cls, abs_filename : str, dev_t : str = 'ram0'):
        return cls.super_table.get(dev_t).do_rmdir(abs_filename)

    @classmethod
    def mknod(cls, abs_filename : str, major : int, minor : int, dev_t : str = 'ram0'):
        return cls.super_table.get(dev_t).do_mknod(abs_filename, major, minor)

    @classmethod
    def fsynch(cls, dev_t : str = 'ram0'):
        cls.super_table.get(dev_t).do_fsynch()

