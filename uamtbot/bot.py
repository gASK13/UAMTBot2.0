import time
import os
from .poster.poster import Poster


class UamtBot:
    def __init__(self):
        self.poster = Poster()

    def app_id(self):
        return os.environ['APP_ID'] if 'APP_ID' in os.environ else 'N/A'

    def handle_command(self, command, options, user, token):
        if command == 'slap':
            self.post_response("Sorry, " + self.get_user(user) + ", can't slap **" + options[0].get(
                'value') + "** yet. Ask <@412352063125717002> to fix this!", token)
            return
        elif command == 'post':
            if user.get('id') == '412352063125717002':
                self.post_response("Bots dispatched...", token)
                time.sleep(10)
                self.post_to_channel(options)
                self.post_response("Bots have delivered their payload.", token)
            else:
                self.post_response("Sorry, Dave, I cannot do that.", token)
        elif command == 'sleep':
            dur = options[0].get('value')
            if dur > 20 or dur < 0:
                self.post_response("Sorry. Can't sleep that long, maximum 20 seconds....", token)
                return
            for i in range(0, dur):
                self.post_response("Sleeping for " + str(i) + " seconds...", token)
                time.sleep(1)
            self.post_response("I'm done now, " + self.get_user(user) + ", are you happy?", token)
            return
        else:
            self.post_response("BORK BORK boooooork .... ", token)
            return

    def get_user(self, user):
        if user is not None:
            if user.get('nick') is not None:
                return user.get('nick')
            elif user.get('user') is not None:
                return user.get('user').get('username')
        return '?$#@'

    def post_response(self, content, token):
        # POST makes "NEW REPLY", PATCH makes "EDIT REPLY" (multiple windows vs one!!!)
        self.poster.patch(
            url='https://discord.com/api/v8/webhooks/' + self.app_id() + '/' + token + "/messages/@original",
            json={
                "content": content,
                "allowed_mentions": {
                    "parse": []
                }
            })

    def post_to_channel(self, options):
        r = self.poster.post(
            url='https://discord.com/api/v8/channels/' + options[0].get('value') + '/messages',
            json={
                "content": options[1].get('value'),
                "allowed_mentions": {
                    "users": [options[2].get('value')]
                }
            })
        print(r)
        print(r.json())
