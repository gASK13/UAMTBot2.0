from uamtbot.commands.usercommand import UserCommand
from datetime import datetime
from uamtbot.commands.age import AgeCommand as ac


class AgeCommand(UserCommand):
    @staticmethod
    def name():
        return 'age'

    @staticmethod
    def handle(body):
        if 'resolved' in body['data']:
            resolved = body['data']['resolved']
            for user_id in resolved['users'].keys():
                if 'members' in resolved:
                    if user_id in resolved['members']:
                        join = datetime.fromisoformat(resolved['members'][user_id]['joined_at'])
                        delta = datetime.now(join.tzinfo) - join
                        settings = ac.get_settings(user_id)
                        if ac.can_show(settings):
                            return AgeCommand.generate_reply(f"<@{user_id}> has been a member of this server for " + str(delta.days) + " days.")
                        else:
                            return AgeCommand.generate_reply(f"<@{user_id}>'s age is private.\n{ac.get_message(settings)}")
                return AgeCommand.generate_reply(f'{resolved["users"][user_id]["username"]} is no longer with us....')
        return AgeCommand.generate_reply("..... I'm not sure what I am supposed to do?")

