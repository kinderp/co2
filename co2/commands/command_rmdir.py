from co2.commands import Command

class CommandRmdir(Command):
    def init(self, argsubparsers):
        argsp = argsubparsers.add_parser("rmdir", help="Remove a directory")

    def execute(self, args):
        print("rmdir...")


    def __init__(self, argsubparsers):
        self.init(argsubparsers)
