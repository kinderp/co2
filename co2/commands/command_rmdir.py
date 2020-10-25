from co2.commands import Command
from co2.commands import CO2Commands
from co2.ipc import Client
from co2.ipc.messages import MessagesFactory

class CommandRmdir(Command):

    def execute(self, args):
        client = Client()
        client.execute(
            MessagesFactory.create(
                CO2Commands.CO2_RMDIR,
                CO2Commands.look_up(CO2Commands.CO2_RMDIR),
                args,
            ).to_dict()
        )
