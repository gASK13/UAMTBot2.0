import unittest
from unittest.mock import MagicMock
from uamtbot import UamtBot


class TestBotHandler(unittest.TestCase):

    def setUp(self):
        self.bot = UamtBot()
        self.bot.poster = MagicMock()

    def test_slap_w_nick(self):
        self.bot.handle_command('slap', {'options': [{'value': 'test test'}]}, {'nick': 'NICK'}, 'token')
        self.bot.poster.patch.assert_called_with(url='https://discord.com/api/v8/webhooks/N/A/token/messages/@original',
                                                 json={
                                                     'content': "Sorry, NICK, can't slap **test test** yet. Ask "
                                                                "<@412352063125717002> to fix this!",
                                                     'allowed_mentions': {'parse': []}})

    def test_slap_no_nick(self):
        self.bot.handle_command('slap', {'options': [{'value': 'test test'}]},
                                {'nick': None, 'user': {'username': 'Name not found'}}, 'token')
        self.bot.poster.patch.assert_called_with(url='https://discord.com/api/v8/webhooks/N/A/token/messages/@original',
                                                 json={
                                                     'content': "Sorry, Name not found, can't slap **test test** yet. Ask "
                                                                "<@412352063125717002> to fix this!",
                                                     'allowed_mentions': {'parse': []}})

    def test_slap_no_user(self):
        self.bot.handle_command('slap', {'options': [{'value': 'test test'}]}, {}, 'token')
        self.bot.poster.patch.assert_called_with(url='https://discord.com/api/v8/webhooks/N/A/token/messages/@original',
                                                 json={
                                                     'content': "Sorry, ?$#@, can't slap **test test** yet. Ask "
                                                                "<@412352063125717002> to fix this!",
                                                     'allowed_mentions': {'parse': []}})
