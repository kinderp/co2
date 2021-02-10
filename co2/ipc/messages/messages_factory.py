from .message import CO2Messages
from .message import MessageSuccess, MessageError
from .message_touch import MessageTouch
from .message_rm import MessageRm
from .message_mkdir import MessageMkdir
from .message_rmdir import MessageRmdir
from .message_tree import MessageTree


class MessagesFactory:
    factory = {
        CO2Messages.CO2_SUCCESS : MessageSuccess,
        CO2Messages.CO2_ERROR   : MessageError,
        CO2Messages.CO2_TOUCH   : MessageTouch,
        CO2Messages.CO2_RM      : MessageRm,
        CO2Messages.CO2_MKDIR   : MessageRmdir,
        CO2Messages.CO2_RMDIR   : MessageRmdir,
        CO2Messages.CO2_TREE    : MessageTree,
    }

    @classmethod
    def create(cls, code, description, args):
        return cls.factory[code](code, description, args)
