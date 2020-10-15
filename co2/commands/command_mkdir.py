from co2.commands import Command

class CommandMkdir(Command):
    def init(self, argsubparsers):
        argsp = argsubparsers.add_parser("mkdir", help="Create a new directory")

    def execute(self, args):
        print("mkdir...")

    def __init__(self, argsubparsers):
        self.init(argsubparsers)


