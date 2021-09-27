import requests
import os


class Poster:
    authConfig = {'Authorization': os.environ['BOT_TOKEN'] if 'BOT_TOKEN' in os.environ else 'N/A'}
    APP_ID = os.environ['APP_ID'] if 'APP_ID' in os.environ else 'N/A'
    API_URL = 'https://discord.com/api/v9/'
    POST_TO_CHANNEL = '{api_url}/channels/{channel_id}/messages'
    PATCH_MESSAGE = '{api_url}/webhooks/{app_id}/{token}/messages/{msg_id}'
    POST_MESSAGE = '{api_url}/webhooks/{app_id}/{token}/messages'

    def __init__(self):
        pass

    @staticmethod
    def patch_message(token, message, message_id='@original'):
        url = Poster.PATCH_MESSAGE.format(app_id=Poster.APP_ID, api_url=Poster.API_URL, token=token, msg_id=message_id)
        print("PATCH to " + url)
        print(str(message))
        return requests.patch(url=url, json=message, headers=Poster.authConfig)

    @staticmethod
    def post_message(token, message):
        url = Poster.POST_MESSAGE.format(app_id=Poster.APP_ID, api_url=Poster.API_URL, token=token)
        print("POST REPLY to " + url)
        print(str(message))
        return requests.post(url=url, json=message, headers=Poster.authConfig)

    @staticmethod
    def post_to_channel(channel_id, message):
        url = Poster.POST_TO_CHANNEL.format(api_url=Poster.API_URL, channel_id=channel_id)
        print("POST CHANNEL to " + url)
        print(str(message))
        return requests.post(url=url, json=message, headers=Poster.authConfig)