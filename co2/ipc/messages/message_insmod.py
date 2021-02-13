from .message import Message

class MessageInsmod(Message):
    def __init__(self, code, description, args):
        super().__init__(code, description, args)
        self.s_dev = args.s_dev
        self.module = args.module
