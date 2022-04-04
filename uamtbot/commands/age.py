from uamtbot.commands.command import Command
from uamtbot.utils.dynastore import DynaStore

class AgeCommand(Command):

    @staticmethod
    def ephemeral():
        return True

    @staticmethod
    def name():
        return 'age'

    @staticmethod
    def get_settings(id):
        user_settings = DynaStore(table_name='user_settings').get(key=id)
        if user_settings is None:
            user_settings = {}
        return user_settings

    @staticmethod
    def store(id, value):
        DynaStore(table_name='user_settings').store(id, value)

    @staticmethod
    def can_show(settings):
        return 'age' not in settings or 'show' not in settings['age'] or settings['age']['show'] == True

    @staticmethod
    def get_message(settings):
        return settings['age']['message']

    @staticmethod
    def handle(body):
        subcommand = body['data']['options'][0]['name']
        user_id = body['member']['user']['id']
        if subcommand == 'show':
            settings = AgeCommand.get_settings(user_id)
            settings['age'] = {'show': True}
            AgeCommand.store(user_id, settings)
            return AgeCommand.generate_reply('Your age is now public.')
        elif subcommand == 'status':
            settings = AgeCommand.get_settings(user_id)
            if AgeCommand.can_show(settings):
                return AgeCommand.generate_reply('Your age is public.')
            else:
                return AgeCommand.generate_reply(f'Your age is hidden with custom message:\n```{AgeCommand.get_message(settings)}```.')
        elif subcommand == 'hide':
            settings = AgeCommand.get_settings(user_id)
            settings['age'] = {'show': False, 'message': body['data']['options'][0]['options'][0]['value']}
            AgeCommand.store(user_id, settings)
            return AgeCommand.generate_reply(f'Your age is now hidden with custom message:\n```{AgeCommand.get_message(settings)}```.')

        return AgeCommand.generate_reply('Hm, seems like you found a hole in my commands?')

