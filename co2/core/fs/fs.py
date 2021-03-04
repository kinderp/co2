import shelve

import co2
from co2.core.fs.superblock import Superblock
from co2.core.fs.t_node import TNode
from co2.core.fs.block import Block
from co2.core.fs.types import Types


class OFlags:
    # File access mode for open()
    O_RDONLY = 0 # Open read-only
    O_WRONLY = 1 # Open write-only
    O_RDWR   = 2 # Open read-write

    # Bits OR'd in the 2nd argument of Open
    O_CREAT = 0x00200 # 512


class TraverseCases:
        CASE_1 = 0
        CASE_2 = 1
        CASE_3 = 2

class HandlersTypes:
        ADD_A_NODE    = 0
        DEL_A_NODE    = 1
        OPEN_A_NODE   = 2
        MOUNT_A_NODE  = 3
        UMOUNT_A_NODE = 4


class HandlersFunctions:
        @staticmethod
        def add_a_node(case : int, filename : str,
                       t_node : TNode, t_node_number : int, type : Types, major : int=-1, minor :
                       int=-1, s_dev : str = 'ram0') -> int:
            if case == TraverseCases.CASE_1:
                # CASE_1: found a leaf.
                #         already existing mnode
                return -1
            elif case == TraverseCases.CASE_2:
                # CASE_2: not found a leaf
                #         not existing node
                superblock = co2.system_calls.IOSystemCalls.super_table[s_dev].superblock
                file_table = co2.system_calls.IOSystemCalls.file_table
                # 1. get a new tnode number
                #    it'll be the index of the new TNode
                #    in the vector table (superblok.vector)
                free_t_node_number = superblock.reserve_t_node_number()
                # 2. Add a new entry in the vector table
                #
                #    SUPERBLOCK.VECTOR:
                #
                #    +--------------+-------+
                #    |     ...      |  ...  |
                #    +--------------+-------+
                #    | t_node_number| TNode |
                #    +--------------+-------+
                #
                # Note: t_node as input parameter is the TNode
                #       of the father of the new node
                superblock.vector.add_entry(
                    vector_entry_index = free_t_node_number,
                    vector_entry       = TNode(
                                                filename=filename,
                                                block=Block(),
                                                type = type,
                                                major=major,
                                                minor=minor,
                                         )
                )
                # each dir_table for a TNode has 2 reserved entries
                # . : t_node_number of the curent dir 
                # ..: t_node_number of the father of the current dir
                #
                # we need to add those 2 entries in current tnode dir_table
                node_dir_table = superblock.vector.get_entry(free_t_node_number).dir_table
                node_dir_table._add(free_t_node_number, ".")
                node_dir_table._add(t_node_number, "..")

                # 3. Add a new entry in the dir_table of the tnode
                # of the father
                t_node.add_dir_entry(free_t_node_number, filename)
                # 4. Add a new entry in the file table
                file_table_number = file_table.add_entry(free_t_node_number, s_dev)
                #return True
                return file_table_number
            elif case == TraverseCases.CASE_3:
                # CASE_3: Not found path
                return -1
            else:
                # Not supported cases
                return -1

        @staticmethod
        def del_a_node(case : int, filename : str, t_node : TNode,
                       t_node_number : int, s_dev : str = 'ram0') -> int:
            if case == TraverseCases.CASE_1:
                superblock = co2.system_calls.IOSystemCalls.super_table[s_dev].superblock
                superblock.release_t_node_number(t_node_number)
                superblock.vector.rem_entry(t_node_number)
                return 1
            elif case == TraverseCases.CASE_2:
                return -1
            elif case == TraverseCases.CASE_3:
                return -1
            else:
                # Not supported cases
                return -1

        @staticmethod
        def open_a_node(case : int, t_node_number : int, s_dev : str = "ram0") -> int:
            if case == TraverseCases.CASE_1:
                superblock = co2.system_calls.IOSystemCalls.super_table[s_dev].superblock
                t_node = superblock.vector.get_entry(t_node_number)
                # CASE_1: found a leaf.
                file_table = co2.system_calls.IOSystemCalls.file_table
                # Add a new entry in the file table
                file_table_number = file_table.add_entry(t_node_number)
                # Add TNode.count (a new fd point to this t_node)
                t_node.count += 1
                return file_table_number
            elif case == TraverseCases.CASE_2:
                # CASE_2_ not found a leaf
                return -1
            elif case == TraverseCases.CASE_3:
                # CASE_3: Not found path
                return -1
            else:
                # Not supported cases
                return -1

        @staticmethod
        def mount_a_node(case : int, t_node : TNode, s_dev : str = 'ram0'):
            if case == TraverseCases.CASE_1:
                t_node.is_mount_point = True
                t_node.s_dev = s_dev

                is_loaded = co2.system_calls.IOSystemCalls.load_superblock(s_dev=s_dev,
                                                        s_imount=t_node)
                if not is_loaded:
                    return False

                return True
            elif case == TraverseCases.CASE_2:
                return False
            elif case == TraverseCases.CASE_3:
                return False
            else:
                # Not supported cases
                return False

        @staticmethod
        def umount_a_node(case : int, t_node : TNode,
                          t_node_number : int, s_dev : str = 'ram0'):
            if case == TraverseCases.CASE_1:
                is_loaded = co2.system_calls.IOSystemCalls.is_superblock_loaded(s_dev=s_dev)
                t_node.is_mount_point = False
                t_node.s_dev = None
                co2.system_calls.IOSystemCalls.unload_superblock(s_dev)
                if not is_loaded:
                    return False
                return True
            elif case == TraverseCases.CASE_2:
                return False
            elif case == TraverseCases.CASE_3:
                return False
            else:
                # Not supported cases
                return False


class Fs:

    def __init__(self, s_dev, s_imount):
        self.superblock = Superblock(s_dev, s_imount)

        self.handlers = {
            HandlersTypes.ADD_A_NODE   : HandlersFunctions.add_a_node,
            HandlersTypes.DEL_A_NODE   : HandlersFunctions.del_a_node,
            HandlersTypes.OPEN_A_NODE  : HandlersFunctions.open_a_node,
            HandlersTypes.MOUNT_A_NODE : HandlersFunctions.mount_a_node,
            HandlersTypes.UMOUNT_A_NODE: HandlersFunctions.umount_a_node,
        }


    def render(self, t_node_number, _prefix="", _last=True, level=0,
               s_dev="ram0"):
        current_superblock = co2.system_calls.IOSystemCalls.super_table[s_dev].superblock
        t_node = current_superblock.vector.get_entry(t_node_number)

        if t_node.is_mount_point:
            if level==0:
                print("   " + t_node.filename + " [m->{}]".format(t_node.s_dev))
            else:
                print(_prefix, "+- " if _last else "|- ", t_node.filename +
                      " [m->{}]".format(t_node.s_dev), sep="")
            s_dev=t_node.s_dev
            self.render(0, _prefix, _last, level+1, s_dev)
        else:
            if level==0:
                print("   " + t_node.filename)
            else:
                if t_node.filename != "/":
                    print(_prefix, "+- " if _last else "|- ", t_node.filename, sep="")
        _prefix += "   " if _last else "|  "
        child_count = len(t_node.dir_table.table.keys())
        for i, child in enumerate(t_node.dir_table.table.keys()):
            _last = i == (child_count - 1)
            t_child_node_number = t_node.dir_table.table[child]
            self.render(t_child_node_number, _prefix, _last, level+1, s_dev)

    def tree_2_json(self):
        map = {}
        for elem, level, t_n, p_n in co2.system_calls.IOSystemCalls.super_table['ram0']._traverse_tree(0, -1):
            if t_n not in map:
                map[t_n] = {"f": elem.filename, "c": [], "l":level}
            if p_n != -1:
                map[p_n]['c'].append(t_n)
        return map

    def _traverse_tree(self, t_node_number : int, p_t_node_number : int, level : int = 0, s_dev : str = "ram0"):
        current_superblock = co2.system_calls.IOSystemCalls.super_table[s_dev].superblock
        t_node = current_superblock.vector.get_entry(t_node_number)
        print(t_node.filename)
        yield t_node, level, t_node_number, p_t_node_number
        level += 1
        for filename, next_t_node_number in t_node.dir_table.table.items():
            next_t_node = current_superblock.vector.get_entry(next_t_node_number)
            if  next_t_node.is_mount_point:
                t_node_mount_point = current_superblock.vector.get_entry(next_t_node_number)
                s_dev = next_t_node.s_dev
                mount_t_node_number = 0
                yield from self._traverse_tree(mount_t_node_number,
                                               t_node_number, level, s_dev)
            yield from self._traverse_tree(next_t_node_number, t_node_number, level, s_dev)



    def _traverse_path(self, path_tokens             : list,
                             level                   : int,
                             t_node_number           : int,
                             handler_type            : int,
                             handler_function_kwargs : dict,
                             s_dev                   : str = "ram0"
                      ):
        """Traverse recursively the whole filesystem tree applying handler_function_kwargs

        Args:
            path_tokens: absolute path to be traversed splitted in tokens ('/'
            as delimeter)

                e.g.
                    '/mnt/hda/doc/test'
                    path_tokens = ['mnt', 'hda', 'doc', 'test']

            level: level of recursion, defined by current path_token 

                e.g.
                    '/mnt/hda/doc/test'
                       ^   ^   ^   ^
                       |   |   |   |
           level=0 --- +   |   |   |
           level=1 --------+   |   |
           level=2 ------------+   |
           level=3 ----------------+

            t_node_number: it's really similar to an inode number on a real
                           filesystem.

                           Each device has a superblock.
                           A superblock contains a TNode(s)' vector, we'll call it
                           just Vector.
                           Vector is composed by two fields:
                               1. t_node_number ( 0 is reserved for root dir '/')
                               2. a pointer to a TNode object.
                                  Inside a TNode does exist a dir_table that
                                  matches filenames with corresponding
                                  t_node_number

                           SUPERBLOCK.VECTOR              TNODE.DIR_TABLE
                           +-----+-----+                  +-----+-----+
                           | 0   | (*) |----------------->| mnt | 100 |
                           +-----+-----+                  +-----+-----+  +-----+----+
                           | 100 | (*) |-------------------------------->| hda | 24 |
                           +-----+-----+           +-----+----+          +-----+----+
                           | 24  | (*) |---------->| doc | 35 |
                           +-----+-----+           +-----+----+
                           | 35  | (*) |
                           +-----+-----+

            handler_type: Type of operation we wanna apply to target Node
                          e.g.
                                HandlersTypes.ADD_A_NODE
                                HandlersTypes.DEL_A_NODE
                                HandlersTypes.OPEN_A_NODE
                                HandlersTypes.DEL_A_NODE
                                HandlersTypes.MOUNT_A_NODE
                                HandlersTypes.UMOUNT_A_NODE

            handler_function_kwargs: kwargs passed to handler_type function
                                     once a target node is reached out

            s_dev: It's a superblock device identifier in the super_table.
                   Each device has a superblock that will be loaded by fs core
                   classes in a datastructure (just a dict) called super_table.
                   Once a mount_point will be encounterd during traversing path
                   s_dev will be changed to that one for the device moutend
                   upon.


        Returns:
                True of False
        Raises:
        """
        current_branch = path_tokens[level]
        current_superblock = co2.system_calls.IOSystemCalls.super_table[s_dev].superblock
        t_node = current_superblock.vector.get_entry(t_node_number)

        next_t_node_number = t_node.dir_table._get(current_branch)
        next_t_node = current_superblock.vector.get_entry(next_t_node_number)

        if  next_t_node_number is not None and next_t_node.is_mount_point:
            if handler_type == HandlersTypes.UMOUNT_A_NODE and next_t_node.s_dev == handler_function_kwargs['s_dev']:
                t_node_mount_point = current_superblock.vector.get_entry(next_t_node_number)
                handler_function_kwargs.update({"t_node" : t_node_mount_point})
                handler_function_kwargs.update({"t_node_number" : next_t_node_number} )
                return self.handlers[handler_type](TraverseCases.CASE_1, **handler_function_kwargs)

            s_dev = next_t_node.s_dev
            mount_path_tokens = path_tokens[level+1:]
            level = 0
            mount_t_node_number = 0
            return self._traverse_path(mount_path_tokens, level,
                                       mount_t_node_number, handler_type,
                                       handler_function_kwargs,
                                       s_dev
            ) 
        if next_t_node_number is not None  and (level + 1 ) == len(path_tokens):
            # Case#1: Found a leaf
            #
            # ADD_A_NODE    : File already exist  KO
            # OPEN_A_NODE   : File found          OK
            # DEL_A_NODE    : File found          OK
            # MOUNT_A_NODE  : File found          OK
            # UMOUNT_A_NODE : File found          OK
            if handler_type == HandlersTypes.ADD_A_NODE:
                handler_function_kwargs.update({"s_dev" : s_dev} )
                return self.handlers[handler_type](TraverseCases.CASE_1, **handler_function_kwargs)
            elif handler_type == HandlersTypes.OPEN_A_NODE:
                handler_function_kwargs.update({"s_dev"         : s_dev        })
                handler_function_kwargs.update({"t_node_number" : next_t_node_number})
                return self.handlers[handler_type](TraverseCases.CASE_1, **handler_function_kwargs)
            elif handler_type == HandlersTypes.DEL_A_NODE:
                handler_function_kwargs.update({"s_dev" : s_dev} )
                handler_function_kwargs.update({"filename"      : current_branch}     )
                handler_function_kwargs.update({"t_node"        : t_node}             )
                handler_function_kwargs.update({"t_node_number" : next_t_node_number} )
                return self.handlers[handler_type](TraverseCases.CASE_1, **handler_function_kwargs)
            elif handler_type == HandlersTypes.MOUNT_A_NODE:
                t_node_mount_point = current_superblock.vector.get_entry(next_t_node_number)
                handler_function_kwargs.update({"t_node" : t_node_mount_point})
                return self.handlers[handler_type](TraverseCases.CASE_1, **handler_function_kwargs)
            elif handler_type == HandlersTypes.UMOUNT_A_NODE:
                t_node_mount_point = current_superblock.vector.get_entry(next_t_node_number)
                handler_function_kwargs.update({"t_node" : t_node_mount_point})
                handler_function_kwargs.update({"t_node_number" : next_t_node_number} )
                return self.handlers[handler_type](TraverseCases.CASE_1, **handler_function_kwargs)
            else:
                pass
        elif next_t_node_number is None and (level + 1) == len(path_tokens):
            # Case#2: Not found a leaf
            #
            # ADD_A_NODE    : does not exist a file with the same name OK
            # OPEN_A_NODE   : file does not exist                      KO
            # DEL_A_NODE    : file does not exist                      KO
            # MOUNT_A_NODE  : fiel does not exist                      KO
            # UMOUNT_A_NODE : fiel does not exist                      KO
            if handler_type == HandlersTypes.ADD_A_NODE:
                handler_function_kwargs.update({"s_dev"        : s_dev          })
                handler_function_kwargs.update({"filename"     : current_branch })
                handler_function_kwargs.update({"t_node"       : t_node         })
                handler_function_kwargs.update({"t_node_number": t_node_number  })
                return self.handlers[handler_type](TraverseCases.CASE_2, **handler_function_kwargs)
            elif handler_type == HandlersTypes.OPEN_A_NODE:
                handler_function_kwargs.update({"s_dev"         : s_dev        })
                handler_function_kwargs.update({"t_node_number" : t_node_number})
                return self.handlers[handler_type](TraverseCases.CASE_2, **handler_function_kwargs)
            elif handler_type == HandlersTypes.DEL_A_NODE:
                handler_function_kwargs.update({"s_dev" : s_dev} )
                return self.handlers[handler_type](TraverseCases.CASE_2, **handler_function_kwargs)
            elif handler_type == HandlersTypes.MOUNT_A_NODE:
                return self.handlers[handler_type](TraverseCases.CASE_2, **handler_function_kwargs)
            elif handler_type == HandlersTypes.UMOUNT_A_NODE:
                handler_function_kwargs.update({"t_node_number": current_branch} )
                handler_function_kwargs.update({"t_node"  : t_node}         )
                return self.handlers[handler_type](current_superblock,
                                                  TraverseCases.CASE_2, **handler_function_kwargs)
            else:
                pass
        elif next_t_node_number is None and (level + 1) < len(path_tokens):
            # Case#3: Not found path
            #
            # ADD_A_NODE    : Path does not exist     KO
            # OPEN_A_NODE   : Path does not exist     KO
            # DEL_A_NODE    : Path does not exist     KO
            # MOUNT_A_NODE  : fiel does not exist     KO
            # UMOUNT_A_NODE : fiel does not exist     KO
            handler_function_kwargs.update({"s_dev" : s_dev} )
            return self.handlers[handler_type](TraverseCases.CASE_3, **handler_function_kwargs)
        else:
            return self._traverse_path(path_tokens, level + 1,
                                       next_t_node_number, handler_type,
                                       handler_function_kwargs, s_dev)

    def _new_node(self, filename : str, type : Types, major : int=-1, minor : int=-1):
        #filename = self._build_abs_path(filename)
        filename = co2.system_calls.ProcessSystemCalls._build_abs_path(filename)
        path_tokens = filename.split("/")[1:]
        return self._traverse_path(path_tokens, 0, 0,
                                   HandlersTypes.ADD_A_NODE,
                                   {
                                        "filename" : None,
                                        "t_node"   : None,
                                        "type"     : type,
                                        "major"    : major,
                                        "minor"    : minor,
                                   },
                                  )
    """
    def _build_abs_path(self, filename : str) -> str:
        if filename.startswith("/"):
            return filename
        else:
            return co2.system_calls.ProcessSystemCalls.C_TASK.PWD + filename
    """

    def _eat_path(self, filename : str):
        #filename = self._build_abs_path(filename)
        filename = co2.system_calls.ProcessSystemCalls._build_abs_path(filename)
        path_tokens = filename.split("/")[1:]
        return self._traverse_path(path_tokens, 0, 0,
                                   HandlersTypes.OPEN_A_NODE, {})

    def _del_node(self, filename : str):
        #filename = self._build_abs_path(filename)
        filename = co2.system_calls.ProcessSystemCalls._build_abs_path(filename)
        path_tokens = filename.split("/")[1:]
        return self._traverse_path(path_tokens, 0, 0,
                                   HandlersTypes.DEL_A_NODE,
                                   {
                                       "filename"      : None,
                                       "t_node"        : None,
                                       "t_node_number" : None,
                                   }
                                  )

    def _mount_node(self, dev_t : str, mount_point : str):
        #mount_point = self._build_abs_path(mount_point)
        mount_point = co2.system_calls.ProcessSystemCalls._build_abs_path(mount_point)
        path_tokens = mount_point.split("/")[1:]
        return self._traverse_path(path_tokens, 0, 0,
                                   HandlersTypes.MOUNT_A_NODE, {"s_dev": dev_t})

    def _umount_node(self, dev_t : str, mount_point : str):
        #mount_point = self._build_abs_path(mount_point)
        mount_point = co2.system_calls.ProcessSystemCalls._build_abs_path(mount_point)
        path_tokens = mount_point.split("/")[1:]
        return self._traverse_path(path_tokens, 0, 0,
                                   HandlersTypes.UMOUNT_A_NODE, {"s_dev": dev_t})

    def do_open(self, abs_filename : str,
                           oflags : OFlags,
                           type   : Types=Types.REGULAR):
        if oflags & OFlags.O_CREAT:
            # Create a new TNode, _calling new_node()
            return self._new_node(abs_filename, type)
        return self._eat_path(abs_filename)

    def do_mkdir(self, abs_filename, oflags : OFlags):
        if oflags & OFlags.O_CREAT:
            return self.do_open(abs_filename, OFlags.O_WRONLY | OFlags.O_CREAT,
                               Types.DIRECTORY)
        return self.do_open(abs_filename, oflags, Types.DIRECTORY)

    def do_rmdir(self, abs_filename : str):
        return self._del_node(abs_filename)

    def do_unlink(self, abs_filename : str):
        return self._del_node(abs_filename)

    def do_mknod(self, abs_filename : str, major : int, minor : int):
        return self._new_node(abs_filename, Types.SPECIAL, major, minor)

    def do_fsynch(self):
        db = shelve.open(".co2_db")
        db[self.superblock.s_dev] = self
        db.close()

    def do_mount(self, dev_t : str, m_point : str):
        block_device_exist = self._eat_path("/dev/{}".format(dev_t))
        if block_device_exist:
            return self._mount_node(dev_t, m_point)
        return False

    def do_umount(self, dev_t : str, m_point : str):
        block_device_exist = self._eat_path("/dev/{}".format(dev_t))
        if block_device_exist:
            return self._umount_node(dev_t, m_point)
        return False

    def do_chdir(self, pathname : str):
        co2.system_calls.ProcessSystemCalls.C_TASK.PWD = None
