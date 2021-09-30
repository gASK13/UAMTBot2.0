from uamtbot.commands.command import Command


class AgeCommand(Command):
    @staticmethod
    def ephemeral():
        return True

    @staticmethod
    def name():
        return 'age'

    @staticmethod
    def handle(body):
        return AgeCommand.generate_reply('Sorry, <@412352063125717002> did not get around to implementing it yet.')

