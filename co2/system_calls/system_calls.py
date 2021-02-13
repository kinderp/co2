from pathlib import Path
import shelve
from co2.core.fs import TNode
from co2.core.fs import Types as FilesTypes
from co2.core.fs import OFlags
from co2.core.fs import Fs
from co2.utils.util import Capturing

from co2.core.fs import DMap

class DriverSystemCalls:
    dmap = DMap()

    @classmethod
    def insmod(self):
        pass

    def rmmod(self):
        pass


class IOSystemCalls:
    Path(".co2/objects").mkdir(parents=True, exist_ok=True)
    db = shelve.open(".co2/objects/co2")

    super_table = {
        'ram0': Fs(s_dev='ram0', s_imount=None)
    }

    @classmethod
    def is_superblock_loaded(cls, s_dev : str) -> bool:
        if s_dev in cls.super_table:
            return True
        return False

    @classmethod
    def unload_superblock(cls, s_dev : str) -> bool:
        if s_dev in cls.super_table:
            cls.super_table.get(s_dev).do_fsynch()
            cls.super_table.pop(s_dev, None)
        return True

    @classmethod
    def load_superblock(cls, s_dev : str, s_imount : TNode) -> bool:
        if s_dev in cls.super_table:
            # dev_t is already mounted on
            return False
        if s_dev in cls.db:
            cls.super_table[s_dev] = cls.db[s_dev]
            cls.super_table[s_dev].s_imount = s_imount
        else:
            cls.super_table[s_dev] = Fs(s_dev=s_dev,
                                        s_imount=s_imount)
        return True


    @classmethod
    def init(cls):
        if 'ram0' in cls.db:
            cls.super_table['ram0'] = cls.db['ram0']
        else:
            cls.mkdir("/dev", dev_t='ram0')
            #cls.mknod("/dev/hda", 1, 2, dev_t='ram0')
            #cls.mknod("/dev/console", 3, 4, dev_t='ram0')

    @classmethod
    def tree(cls):
        with Capturing() as output:
            cls.super_table["ram0"].render(0, s_dev="ram0")
        return output

    @classmethod
    def open(cls, abs_filename : str, oflags : OFlags = OFlags.O_CREAT | OFlags.O_WRONLY, dev_t : str = 'ram0'):
        return cls.super_table.get(dev_t).do_open(abs_filename, oflags, FilesTypes.REGULAR)

    @classmethod
    def unlink(cls, abs_filename : str, dev_t : str = 'ram0'):
        return cls.super_table.get(dev_t).do_unlink(abs_filename)

    @classmethod
    def mkdir(cls, abs_filename : str, dev_t : str = 'ram0'):
        return cls.super_table.get(dev_t).do_mkdir(abs_filename,  OFlags.O_WRONLY | OFlags.O_CREAT)

    @classmethod
    def rmdir(cls, abs_filename : str, dev_t : str = 'ram0'):
        return cls.super_table.get(dev_t).do_rmdir(abs_filename)

    @classmethod
    def mknod(cls, abs_filename : str, major : int, minor : int, dev_t : str = 'ram0'):
        return cls.super_table.get(dev_t).do_mknod(abs_filename, major, minor)

    @classmethod
    def fsynch(cls, dev_t : str = 'ram0'):
        cls.super_table.get(dev_t).do_fsynch()

    @classmethod
    def mount(cls, dev_t : str, m_point : str):
        return cls.super_table.get('ram0').do_mount(dev_t, m_point)

    @classmethod
    def umount(cls, dev_t : str, m_point : str):
        return cls.super_table.get('ram0').do_umount(dev_t, m_point)
