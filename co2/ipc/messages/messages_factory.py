from co2.commands import CO2Commands

from .message_touch import MessageTouch
from .message_rm import MessageRm
from .message_mkdir import MessageMkdir
from .message_rmdir import MessageRmdir

class MessagesFactory:
    factory = {
        CO2Commands.CO2_TOUCH: MessageTouch,
        CO2Commands.CO2_RM   : MessageRm,
        CO2Commands.CO2_MKDIR: MessageRmdir,
        CO2Commands.CO2_RMDIR: MessageRmdir,
    }

    @classmethod
    def create(cls, code, description, args):
        return cls.factory[code](code, description, args)
