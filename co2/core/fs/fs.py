from co2.core.fs import Superblock
from co2.core.fs import TNode
from co2.core.fs import Block
from co2.core.fs import Types

class OFlags:
    # File access mode for open()
    O_RDONLY = 0 # Open read-only
    O_WRONLY = 1 # Open write-only
    O_RDWR   = 2 # Open read-write

    # Bits OR'd in the 2nd argument of Open
    O_CREAT = 0x00200 # 512

class Fs:

    superblock = Superblock()

    @classmethod
    def _traverse_path(cls, path_tokens   : list,
                            level         : int,
                            t_node_number : int,
                            creat         : bool  = False,
                            type          : Types = Types.REGULAR,
                      ):
        current_branch = path_tokens[level]
        t_node = cls.superblock.vector.get_entry(t_node_number)
        next_t_node_number = t_node.dir_table._get(current_branch)
        if not next_t_node_number and (level + 1) == len(path_tokens):
            # New file here, OK.
            if creat:
                free_t_node_number = cls.superblock.reserve_t_node_number()
                cls.superblock.vector.add_entry(
                    vector_entry_index = free_t_node_number,
                    vector_entry       = TNode(filename=current_branch,
                                               block=Block(name=current_branch,
                                                           parent=t_node.block,),
                                               type = type
                                         )
                )
                t_node.add_dir_entry(free_t_node_number, current_branch)
                return True
            else:
                # filename doesn't exist
                return False
        elif not next_t_node_number and (level + 1) < len(path_tokens):
            # Path does not exist, error!
            return False
        else:
            return cls._traverse_path(path_tokens, level + 1,
                                      next_t_node_number, creat)

    @classmethod
    def _new_node(cls, filename : str, type : Types):
        path_tokens = filename.split("/")[1:]
        return cls._traverse_path(path_tokens, 0, 0, True, type)

    @classmethod
    def _eat_path(cls, filename : str):
        path_tokens = filename.split("/")[1:]
        return cls._traverse_path(path_tokens, 0, 0, False, None)

    @classmethod
    def do_open(cls, abs_filename : str,
                           oflags : OFlags,
                           type   : Types=Types.REGULAR):
        if oflags & OFlags.O_CREAT:
            # Create a new TNode, _calling new_node()
            return cls._new_node(abs_filename, type)
        return cls._eat_path(abs_filename)

    @classmethod
    def do_mkdir(cls, abs_filename):
        cls.do_open(abs_filename, OFlags.O_WRONLY | OFlags.O_CREAT,
                    Types.DIRECTORY)

    def __init__(self):
        pass
