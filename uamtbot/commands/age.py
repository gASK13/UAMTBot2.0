from uamtbot.commands.command import Command


class AgeCommand(Command):
    @staticmethod
    def name():
        return 'age'

    @staticmethod
    def handle(body):
        return super.generate_reply('Sorry, <@412352063125717002> did not get around to implementing it yet.')

