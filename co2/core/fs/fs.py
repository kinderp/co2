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


class TraverseCases:
        CASE_1 = 0
        CASE_2 = 1
        CASE_3 = 2

class HandlersTypes:
        ADD_A_NODE  = 0
        DEL_A_NODE  = 1
        OPEN_A_NODE = 2


class HandlersFunctions:
        @staticmethod
        def add_a_node(superblock : Superblock, case : int, filename : str,
                       t_node : TNode, type : Types, major : int=-1, minor : int=-1):
            if case == TraverseCases.CASE_1:
                return False
            elif case == TraverseCases.CASE_2:
                free_t_node_number = superblock.reserve_t_node_number()
                superblock.vector.add_entry(
                    vector_entry_index = free_t_node_number,
                    vector_entry       = TNode(
                                                filename=filename,
                                                block=Block(
                                                    name=filename,
                                                    parent=t_node.block,
                                                ),
                                                type = type,
                                                major=major,
                                                minor=minor,
                                         )
                )
                t_node.add_dir_entry(free_t_node_number, filename)
                return True
            elif case == TraverseCases.CASE_3:
                return False
            else:
                # Not supported cases
                return False

        @staticmethod
        def del_a_ndoe(superblock : Superblock, case : int, filename : str, t_node : TNode,
                       t_node_number : int):
            if case == TraverseCases.CASE_1:
                superblock.release_t_node_number(t_node_number)
                superblock.vector.rem_entry(t_node_number)
                old_children = list(t_node.block.children) # children it's a tuple :(
                for index, children in enumerate(old_children):
                    if children.name == filename:
                        old_children.pop(index)
                t_node.block.children = old_children
                return True
            elif case == TraverseCases.CASE_2:
                return False
            elif case == TraverseCases.CASE_3:
                return False
            else:
                # Not supported cases
                return False

        @staticmethod
        def open_a_node(superblock : Superblock, case : int):
            if case == TraverseCases.CASE_1:
                return True
            elif case == TraverseCases.CASE_2:
                return False
            elif case == TraverseCases.CASE_3:
                return False
            else:
                # Not supported cases
                return False


class Fs:

    superblock = Superblock()

    handlers = {
        HandlersTypes.ADD_A_NODE  : HandlersFunctions.add_a_node,
        HandlersTypes.DEL_A_NODE  : HandlersFunctions.del_a_ndoe,
        HandlersTypes.OPEN_A_NODE : HandlersFunctions.open_a_node,
    }

    @classmethod
    def _traverse_path(cls, path_tokens            : list,
                            level                   : int,
                            t_node_number           : int,
                            handler_type            : int,
                            handler_function_kwargs : dict,
                      ):
        current_branch = path_tokens[level]
        t_node = cls.superblock.vector.get_entry(t_node_number)
        next_t_node_number = t_node.dir_table._get(current_branch)
        if next_t_node_number and (level + 1 ) == len(path_tokens):
            # Case#1: Found a leaf
            #
            # ADD_A_NODE  : File already exist  KO
            # OPEN_A_NODE : File found          OK
            # DEL_A_NODE  : File found          OK
            if handler_type == HandlersTypes.ADD_A_NODE:
                return cls.handlers[handler_type](cls.superblock,
                                                  TraverseCases.CASE_1, **handler_function_kwargs)
            elif handler_type == HandlersTypes.OPEN_A_NODE:
                return cls.handlers[handler_type](cls.superblock,
                                                  TraverseCases.CASE_1, **handler_function_kwargs)
                pass
            elif handler_type == HandlersTypes.DEL_A_NODE:
                handler_function_kwargs.update({"filename"      : current_branch}     )
                handler_function_kwargs.update({"t_node"        : t_node}             )
                handler_function_kwargs.update({"t_node_number" : next_t_node_number} )
                return cls.handlers[handler_type](cls.superblock,
                                                  TraverseCases.CASE_1, **handler_function_kwargs)
            else:
                pass
        elif not next_t_node_number and (level + 1) == len(path_tokens):
            # Case#2: Not found a leaf
            #
            # ADD_A_NODE  : does not exist a file with the same name OK
            # OPEN_A_NODE : file does not exist                      KO
            # DEL_A_NODE  : file does not exist                      KO
            if handler_type == HandlersTypes.ADD_A_NODE:
                handler_function_kwargs.update({"filename": current_branch} )
                handler_function_kwargs.update({"t_node"  : t_node}         )
                return cls.handlers[handler_type](cls.superblock,
                                                  TraverseCases.CASE_2, **handler_function_kwargs)
            elif handler_type == HandlersTypes.OPEN_A_NODE:
                return cls.handlers[handler_type](cls.superblock,
                                                  TraverseCases.CASE_2, **handler_function_kwargs)
            elif handler_type == HandlersTypes.DEL_A_NODE:
                return cls.handlers[handler_type](cls.superblock,
                                                  TraverseCases.CASE_2, **handler_function_kwargs)
            else:
                pass
        elif not next_t_node_number and (level + 1) < len(path_tokens):
            # Case#3: Not found path
            #
            # ADD_A_NODE  : Path does not exist     KO
            # OPEN_A_NODE : Path does not exist     KO
            # DEL_A_NODE  : Path does not exist     KO
            return cls.handlers[handler_type](cls.superblock,
                                              TraverseCases.CASE_3, **handler_function_kwargs)
        else:
            return cls._traverse_path(path_tokens, level + 1,
                                       next_t_node_number, handler_type,
                                       handler_function_kwargs)

    @classmethod
    def _new_node(cls, filename : str, type : Types, major : int=-1, minor : int=-1):
        path_tokens = filename.split("/")[1:]
        return cls._traverse_path(path_tokens, 0, 0,
                                   HandlersTypes.ADD_A_NODE,
                                   {
                                        "filename" : None,
                                        "t_node"   : None,
                                        "type"     : type,
                                        "major"    : major,
                                        "minor"    : minor,
                                   },
                                  )

    @classmethod
    def _eat_path(cls, filename : str):
        path_tokens = filename.split("/")[1:]
        return cls._traverse_path(path_tokens, 0, 0,
                                   HandlersTypes.OPEN_A_NODE, {})

    @classmethod
    def _del_node(cls, filename : str):
        path_tokens = filename.split("/")[1:]
        return cls._traverse_path(path_tokens, 0, 0,
                                   HandlersTypes.DEL_A_NODE,
                                   {
                                       "filename"      : None,
                                       "t_node"        : None,
                                       "t_node_number" : None,
                                   }
                                  )

    @classmethod
    def do_open(cls, abs_filename : str,
                           oflags : OFlags,
                           type   : Types=Types.REGULAR):
        if oflags & OFlags.O_CREAT:
            # Create a new TNode, _calling new_node()
            return cls._new_node(abs_filename, type)
        return cls._eat_path(abs_filename)

    @classmethod
    def do_mkdir(cls, abs_filename, oflags : OFlags):
        if oflags & OFlags.O_CREAT:
            return cls.do_open(abs_filename, OFlags.O_WRONLY | OFlags.O_CREAT,
                               Types.DIRECTORY)
        return cls.do_open(abs_filename, oflags, Types.DIRECTORY)

    @classmethod
    def do_rmdir(cls, abs_filename : str):
        return cls._del_node(abs_filename)

    @classmethod
    def do_unlink(cls, abs_filename : str):
        return cls._del_node(abs_filename)

    @classmethod
    def do_mknod(cls, abs_filename : str, major : int, minor : int):
        return cls._new_node(abs_filename, Types.SPECIAL, major, minor)

    def __init__(self):
        pass
