from uamtbot.commands.command import Command


class UserCommand(Command):
    @staticmethod
    def type():
        return 2  # type for user command
