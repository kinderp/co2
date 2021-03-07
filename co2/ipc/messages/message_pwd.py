from .message import Message

class MessagePwd(Message):
    def __init__(self, code, description, args):
        super().__init__(code, description, args)
