from co2.commands import Command
from co2.ipc import Client
from co2.ipc.messages import MessagesFactory
from co2.ipc.messages import CO2Messages

import json

class CommandTree(Command):

    def execute(self, args):
        client = Client()
        response = client.execute(
            MessagesFactory.create(
                CO2Messages.CO2_TREE,
                CO2Messages.look_up(CO2Messages.CO2_TREE),
                args,
            )
        )
        response = json.loads(response.decode('utf-8'))
        for line in response['description']:
            print(line)
