import importlib
from inspect import getmembers, isabstract, isclass
import json
from pathlib import Path
import shelve

from co2.core.fs.t_node import TNode
from co2.core.fs.types import Types as FilesTypes
from co2.core.fs.fs import OFlags
from co2.core.fs.fs import Fs
from co2.utils.util import Capturing

from co2.core.fs.d_map import DMap
from co2.core.fs.d_map import DEVICE_MAPPING
from co2.core.fs.f_table import FTable
from co2.core.ps import PTable
from co2.core.ps import PTEntry


#from co2.types import AWS_TYPES
from co2.types.bin.elf import Elf

class ProcessSystemCalls:
    ptable = None
    C_TASK = None

    @classmethod
    def init(cls):
       cls.ptable = PTable()

    @classmethod
    def boot(cls):
        cls.init()
        swapper = PTEntry()
        swapper.PID = "/"
        swapper.PWD = "/"
        cls.ptable.table[swapper.PID] = swapper
        cls.C_TASK = swapper
        # create root fs
        IOSystemCalls.init()
        #file_table_number = IOSystemCalls.mkdir('/')
        #fd = cls.C_TASK.FDTABLE.add(file_table_number)

        file_table_number = IOSystemCalls.mkdir('/bin')
        fd = cls.C_TASK.FDTABLE.add(file_table_number)

        file_table_number = IOSystemCalls.mkdir('/dev')
        fd = cls.C_TASK.FDTABLE.add(file_table_number)

        file_table_number = IOSystemCalls.mknod('/dev/vpc', DEVICE_MAPPING['vpc'], 1)
        fd = cls.C_TASK.FDTABLE.add(file_table_number)

        file_table_number = IOSystemCalls.mkdir('/bin/cdk')
        fd = cls.C_TASK.FDTABLE.add(file_table_number)

        file_table_number = IOSystemCalls.open('/bin/cdk/vpc')
        vpc = importlib.import_module('co2.types.bin.cdk.vpc')
        fd = cls.C_TASK.FDTABLE.add(file_table_number)
        #IOSystemCalls.write(fd, AWS_TYPES("AWS::EC2::VPC"))
        IOSystemCalls.write(fd, vpc)


    @classmethod
    def fork(cls):
        PPID = cls.C_TASK.PID
        PID = cls.C_TASK.PWD
        p = cls.ptable.get_entry(PPID)
        if not p:
            # current task does not exit in ptable
            # something went wrong. We should raise
            # something similar to a kernel panic
            return -1

        e = PTEntry()
        done = cls.ptable.add_entry(PID, e)
        if done:
            cls.ptable[PID].PID = PID
            cls.ptable[PID].PPID = PPID
            cls.ptable[PID].FDTABLE = p.FDTABLE
            return 1
        return -1

    @classmethod
    def execve(cls, abs_filename : str):
        try:
            pwd = cls.C_TASK.PWD
            file_table_number = IOSystemCalls.open(abs_filename, OFlags.O_RDONLY)
            fd = cls.C_TASK.FDTABLE.add(file_table_number)
            buffer = []
            IOSystemCalls.read(fd, buffer, 1)
            # it should be a module, fingers crossed
            block = buffer[0]
            classes = getmembers(block,
                             lambda m: isclass(m) and not isabstract(m))
            executable = None
            for name, _class in classes:
                if issubclass(_class, Elf):
                    executable = _class()
                    break
            if executable:
                executable.text()
        except Exception as e:
            return -1
        return 1

    @classmethod
    def mmap(cls, abs_filename):
        try:
            mapped = json.loads(abs_filename)
        except Exception as e:
            return -1

    @classmethod
    def _build_abs_path(cls, filename : str) -> str:
        def get_template():
            if cls.C_TASK.PWD.endswith("/"):
                pwd_template = "{}{}"
            else:
                pwd_template = "{}/{}"
            return pwd_template

        if filename.startswith(".."):
            pwd_template = get_template()
            return pwd_template.format(cls.C_TASK.PWD, filename)

        if filename.startswith("/"):
            return filename
        else:
            pwd_template = get_template()
            return pwd_template.format(cls.C_TASK.PWD, filename)



class DriverSystemCalls:
    dmap = DMap()

    @classmethod
    def insmod(cls, s_dev : str, module : str) -> bool:
        return cls.dmap.load_item(s_dev, module)

    @classmethod
    def rmmod(cls, s_dev : str) -> bool:
        return cls.dmap.unload_item(s_dev)


class IOSystemCalls:
    Path(".co2/objects").mkdir(parents=True, exist_ok=True)
    db = shelve.open(".co2/objects/co2")

    super_table = None
    file_table  = None

    @classmethod
    def init(cls):
        cls.super_table = {
            'ram0': Fs(s_dev='ram0', s_imount=None)
        }
        cls.file_table = FTable()

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

    """
    @classmethod
    def init(cls):
        if 'ram0' in cls.db:
            cls.super_table['ram0'] = cls.db['ram0']
        else:
            cls.mkdir("/dev", dev_t='ram0')
            #cls.mknod("/dev/hda", 1, 2, dev_t='ram0')
            #cls.mknod("/dev/console", 3, 4, dev_t='ram0')
    """

    @classmethod
    def tree(cls):
        with Capturing() as output:
            cls.super_table["ram0"].render(0, s_dev="ram0")
        return output

    @classmethod
    def open(cls, abs_filename : str, oflags : OFlags = OFlags.O_CREAT | OFlags.O_WRONLY, dev_t : str = 'ram0'):
        return cls.super_table.get(dev_t).do_open(abs_filename, oflags, FilesTypes.REGULAR)

    @classmethod
    def close(cls, fd : int):
        ftable_index = co2.ProcessSystemCalls.C_TASK.FDTABLE.get(fd)
        co2.ProcessSystemCalls.C_TASK.FDTABLE.rem(fd)

        file_table = cls.super_table["ram0"].file_table

        t_node_number = file_table.get_entry(ftable_index)
        t_node = cls.super_table["ram0"].superblock.get_entry(t_node_number)
        t_node.count -= 1

        file_table.rem_entry(t_node_number)

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

    @classmethod
    def write(cls, fd : int, buffer : object, count : int = 1):
        ftable_index = ProcessSystemCalls.C_TASK.FDTABLE.get(fd)
        t_node_number, ft_count, s_dev = cls.file_table.get_entry(ftable_index)
        t_node = cls.super_table[s_dev].superblock.vector.get_entry(t_node_number)
        if t_node.major != -1:
            # retrieve the correct driver from dmap table
            # run write func of the selected driver
            count = DriverSystemCalls.dmap.dmap[t_node.major][1].write(buffer, count)
            return count
        t_node.block.data = buffer
        return count

    @classmethod
    def read(cls, fd : int, buffer : object, count : int = 1):
        ftable_index = ProcessSystemCalls.C_TASK.FDTABLE.get(fd)
        t_node_number, ft_count, s_dev = cls.file_table.get_entry(ftable_index)
        t_node = cls.super_table[s_dev].superblock.vector.get_entry(t_node_number)
        buffer.append(t_node.block.data)
        return count

    @classmethod
    def pwd(cls):
        return ProcessSystemCalls.C_TASK.PWD

    @classmethod
    def chdir(cls, abs_filename : str):
        try:
            pathname = ProcessSystemCalls._build_abs_path(abs_filename)
            ProcessSystemCalls.C_TASK.PWD = pathname
            return 1
        except Exception as e:
            return -1
