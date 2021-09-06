import requests
import os

authConfig = {'Authorization': os.environ['BOT_TOKEN'] if 'BOT_TOKEN' in os.environ else 'N/A'}


class Poster:
    def __init__(self):
        pass

    def patch(self, url, json):
        requests.patch(url=url, json=json, headers=authConfig)

    def post(self, url, json):
        requests.post(url=url, json=json, headers=authConfig)