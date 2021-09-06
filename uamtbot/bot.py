import json
import time
import requests
import os

authConfig = {'Authorization': os.environ['BOT_TOKEN']}


def get_user(user):
    if user.get('nick') is not None:
        return user.get('nick')
    return user.get('user').get('username')


def post_response(content, token):
    # POST makes "NEW REPLY", PATCH makes "EDIT REPLY" (multiple windows vs one!!!)
    requests.patch(
        url='https://discord.com/api/v8/webhooks/' + os.environ['APP_ID'] + '/' + token + "/messages/@original",
        headers=authConfig, json={
            "content": content,
            "allowed_mentions": {
                "parse": []
            }
        })


def post_to_channel(options):
    r = requests.post(
        url='https://discord.com/api/v8/channels/' + options[0].get('value') + '/messages',
        headers=authConfig, json={
            "content": options[1].get('value'),
            "allowed_mentions": {
                "users": [options[2].get('value')]
            }
        })
    print(r)
    print(r.json())


class UamtBot:
    def __init__(self):
        pass

    @staticmethod
    def handle_command(command, options, user, token):
        if command == 'slap':
            post_response("Sorry, " + get_user(user) + ", can't slap **" + options[0].get(
                'value') + "** yet. Ask <@412352063125717002> to fix this!", token)
            return
        elif command == 'post':
            if user.get('id') == '412352063125717002':
                post_response("Bots dispatched...", token)
                time.sleep(10)
                post_to_channel(options)
                post_response("Bots have delivered their payload.", token)
            else:
                post_response("Sorry, Dave, I cannot do that.", token)
        elif command == 'sleep':
            dur = options[0].get('value')
            if dur > 20 or dur < 0:
                post_response("Sorry. Can't sleep that long, maximum 20 seconds....", token)
                return
            for i in range(0, dur):
                post_response("Sleeping for " + str(i) + " seconds...", token)
                time.sleep(1)
            post_response("I'm done now, " + get_user(user) + ", are you happy?", token)
            return
        else:
            post_response("BORK BORK boooooork .... ", token)
            return
