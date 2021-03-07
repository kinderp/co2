from co2.commands import Command
from co2.ipc import Client
from co2.ipc.messages import MessagesFactory
from co2.ipc.messages import CO2Messages

import json

class CommandPwd(Command):

    def execute(self, args):
        client = Client()
        response = client.execute(
            MessagesFactory.create(
                CO2Messages.CO2_PWD,
                CO2Messages.look_up(CO2Messages.CO2_PWD),
                args,
            )
        )
        response = json.loads(response.decode('utf-8'))
        print(response['description'])
