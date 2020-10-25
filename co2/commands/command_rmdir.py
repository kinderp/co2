from co2.commands import Command
from co2.ipc import Client
from co2.ipc.messages import MessagesFactory
from co2.ipc.messages import CO2Messages

class CommandRmdir(Command):

    def execute(self, args):
        client = Client()
        client.execute(
            MessagesFactory.create(
                CO2Commands.CO2_RMDIR,
                CO2Commands.look_up(CO2Commands.CO2_RMDIR),
                args,
            )
        )
