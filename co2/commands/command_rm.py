from co2.commands import Command

class CommandRm(Command):
    def init(self, argsubparsers):
        argsp = argsubparsers.add_parser("rm", help="Remove a file")

    def execute(self, args):
        print("rm...")

    def __init__(self, argsubparsers):
        self.init(argsubparsers)

