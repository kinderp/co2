from .message import Message

class MessageMkdir(Message):
    def __init__(self, code, description, args):
        super().__init__(code, description, args)
        self.abs_filename = args.abs_filename
