messages import MessagesFactory
from co2.ipc.messages import CO2Messages

class CommandMknod(Command):

    def execute(self, args):
        client = Client()
        client.execute(
            MessagesFactory.create(
                CO2Messages.CO2_MKNOD,
                CO2Messages.look_up(CO2Messages.CO2_MKNOD),
                args,
            )
        )
