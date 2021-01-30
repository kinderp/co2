from co2.ipc.messages import MessagesFactory
from co2.ipc.messages import CO2Messages

class CommandMount(Command):

    def execute(self, args):
        client = Client()
        client.execute(
            MessagesFactory.create(
                CO2Messages.CO2_MOUNT,
                CO2Messages.look_up(CO2Messages.CO2_MOUNT),
                args,
            )
        )
