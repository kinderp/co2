from co2.commands import Command
from co2.ipc import Client
from co2.ipc.messages import MessagesFactory
from co2.ipc.messages import CO2Messages

class CommandInsmod(Command):

    def execute(self, args):
        client = Client()
        client.execute(
            MessagesFactory.create(
                CO2Messages.CO2_INSMOD,
                CO2Messages.look_up(CO2Messages.CO2_INSMOD),
                args,
            )
        )
