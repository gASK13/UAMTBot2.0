from uamtbot.commands.usercommand import UserCommand
from datetime import datetime


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
                        return AgeCommand.generate_reply("<@" + user_id + "> has been a member of this server for " + str(delta.days) + " days.")
                return AgeCommand.generate_reply(resolved["users"][user_id]["username"] + " is no longer with us....")
        return AgeCommand.generate_reply("..... I'm not sure what I am supposed to do?")

