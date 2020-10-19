from co2.commands import Command
from co2.commands import CO2Commands
from co2.ipc import Client
from co2.ipc.messages import MessagesFactory

class CommandMkdir(Command):
    def init(self, argsubparsers):
        argsp = argsubparsers.add_parser("mkdir", help="Create a new directory")
        argsp.add_argument("path", help="Remove a file", type=str)

    def execute(self, args):
        client = Client()
        client.execute(
            MessagesFactory.create(
                CO2Commands.CO2_MKDIR,
                CO2Commands.look_up(CO2Commands.CO2_MKDIR),
                args,
            ).to_dict()
        )

    def __init__(self, argsubparsers):
        self.init(argsubparsers)


