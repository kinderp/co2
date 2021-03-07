# IO Messages
from .message import CO2Messages
from .message import MessageSuccess, MessageError
from .message_touch import MessageTouch
from .message_rm import MessageRm
from .message_mkdir import MessageMkdir
from .message_rmdir import MessageRmdir
from .message_tree import MessageTree
from .message_insmod import MessageInsmod
from .message_cd import MessageCd
from .message_pwd import MessagePwd
# PS Mesagess
from .message_boot import MessageBoot

class MessagesFactory:
    factory = {
        # PS Messages
        CO2Messages.CO2_BOOT    : MessageBoot,
        # IO Messages
        CO2Messages.CO2_SUCCESS : MessageSuccess,
        CO2Messages.CO2_ERROR   : MessageError,
        CO2Messages.CO2_TOUCH   : MessageTouch,
        CO2Messages.CO2_RM      : MessageRm,
        CO2Messages.CO2_MKDIR   : MessageRmdir,
        CO2Messages.CO2_RMDIR   : MessageRmdir,
        CO2Messages.CO2_TREE    : MessageTree,
        CO2Messages.CO2_INSMOD  : MessageInsmod,
        CO2Messages.CO2_CD      : MessageCd,
        CO2Messages.CO2_PWD     : MessagePwd,
    }

    @classmethod
    def create(cls, code, description, args):
        return cls.factory[code](code, description, args)
