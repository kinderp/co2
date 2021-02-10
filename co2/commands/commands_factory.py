from .command_touch import CommandTouch
from .command_rm import CommandRm
from .command_mkdir import CommandMkdir
from .command_rmdir import CommandRmdir
from .command_tree import CommandTree

class CommandsFactory:

    COMMANDS = {
        "mkdir": CommandMkdir,
        "rmdir": CommandRmdir,
        "touch": CommandTouch,
        "rm"   :    CommandRm,
        "tree" :  CommandTree,
    }

    @classmethod
    def create(cls, command):
        return cls.COMMANDS[command]()
