from co2.commands import Command
from co2.commands import CO2Commands
from co2.ipc import Client
from co2.ipc.messages import MessagesFactory

class CommandTouch(Command):
    def init(self, argsubparsers):
        argsp = argsubparsers.add_parser("touch", help="Create a new file")
        argsp.add_argument("path", help="Create a file", type=str)

    def execute(self, args):
        client = Client()
        client.execute(
            MessagesFactory.create(
                CO2Commands.CO2_TOUCH,
                CO2Commands.look_up(CO2Commands.CO2_TOUCH),
                args,
            ).to_dict()
        )

    def __init__(self, argsubparsers):
        self.init(argsubparsers)
