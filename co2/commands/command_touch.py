from co2.commands import Command

class CommandTouch(Command):
    def init(self, argsubparsers):
        argsp = argsubparsers.add_parser("touch", help="Create a new file")

    def execute(self, args):
        print("touch...")

    def __init__(self, argsubparsers):
        self.init(argsubparsers)
