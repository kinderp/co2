class Message:
    def __init__(self, code, description, args):
        self.raw_data = args
        self.code = code
        self.description = description

    def to_dict(self):
        pass

