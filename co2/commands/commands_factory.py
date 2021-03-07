# PS Commands
from .command_boot import CommandBoot

# IO Commands
from .command_touch import CommandTouch
from .command_rm import CommandRm
from .command_mkdir import CommandMkdir
from .command_rmdir import CommandRmdir
from .command_tree import CommandTree
from .command_insmod import CommandInsmod
from .command_cd import CommandCd
from .command_pwd import CommandPwd


class CommandsFactory:

    COMMANDS = {
        # PS Commands
        "boot"  :   CommandBoot,
        # IO Commands
        "mkdir" :  CommandMkdir,
        "rmdir" :  CommandRmdir,
        "touch" :  CommandTouch,
        "rm"    :     CommandRm,
        "tree"  :   CommandTree,
        "insmod": CommandInsmod,
        "cd"    :     CommandCd,
        "pwd"   :    CommandPwd,
    }

    @classmethod
    def create(cls, command):
        return cls.COMMANDS[command]()
