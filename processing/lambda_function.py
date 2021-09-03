import json
import time
import requests
import os

authConfig = { 'Authorization': os.environ['BOT_TOKEN'] }

def get_user(body):
    if body.get('member').get('nick') is not None:
        return body.get('member').get('nick')
    return body.get('member').get('user').get('username')

def post_response(content, body):
    # POST makes "NEW REPLY", PATCH makes "EDIT REPLY" (multiple windows vs one!!!)
    requests.patch(url = 'https://discord.com/api/v8/webhooks/' + os.environ['APP_ID'] + '/' + body.get('token') + "/messages/@original", headers = authConfig, data = {
            "content" : content
        })

def post_to_channel():
    requests.post(url = '/channels/' + body.get('data').get('options')[0].get('value') + '/messages', headers = authConfig, data = {
        "content" : body.get('data').get('options')[1].get('value'),
        "allowed_mentions": {
            "users": [body.get('data').get('options')[2].get('value')]
        }
    })

def lambda_handler(event, context):
    print(f"event {event}") # debug print

    # check if message is a ping
    body = event.get('body-json')

    if body.get('data').get('name') == 'slap':
        post_response("Sorry, " + get_user(body) + ", can't slap **" + body.get('data').get('options')[0].get('value') + "** yet. Ask <@412352063125717002> to fix this!", body)
        return
    elif body.get('data').get('name') == 'post':
        if body.get('data').get('member').get('id') == 412352063125717002:
            post_response("Bots dispatched...")
            time.sleep(10)
            //post
        else:
            post_response("Sorry, Dave, I cannot do that.")
    elif body.get('data').get('name') == 'sleep':
        dur = body.get('data').get('options')[0].get('value')
        if dur > 20 or dur < 0:
            post_response("Sorry. Can't sleep that long, maximum 20 seconds....", body)
            return
        for i in range(0, dur):
            post_response("Sleeping for " + str(i) + " seconds...", body)
            time.sleep(1)
        post_response("I'm done now, " + get_user(body) + ", are you happy?", body)
        return
    else:
        post_response("BORK BORK boooooork .... ", body)
        return
