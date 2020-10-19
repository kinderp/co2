from .message import Message

class MessageRm(Message):
    def __init__(self, code, description, args):
        super().__init__(code, description, args)
        self.path = args.path

    def to_dict(self):
        return {
            "code": self.code,
            "description": self.description,
            "data": {
                "path": self.path
            }
        }
