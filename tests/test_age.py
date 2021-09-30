import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from uamtbot.commands.userage import AgeCommand


class TestUserAgeCommand(unittest.TestCase):

    def test_age_member_wrong_json(self):
        response = AgeCommand.handle({'type': 2, 'data': {'name': 'slap', 'type': 2}, 'token': 'token'})
        assert response['content'] == "..... I'm not sure what I am supposed to do?"

    def test_age_member_no_members(self):
        response = AgeCommand.handle(
            {'type': 2, 'data': {'name': 'slap', 'type': 2, 'resolved': {'users': {'1': {'username': 'TEST'}}}},
             'token': 'token'})
        assert response['content'] == "TEST is no longer with us...."

    def test_age_member_empty_members(self):
        response = AgeCommand.handle(
            {'type': 2,
             'data': {'name': 'slap', 'type': 2, 'resolved': {'members': {}, 'users': {'1': {'username': 'TEST'}}}},
             'token': 'token'})
        assert response['content'] == "TEST is no longer with us...."

    def test_age_member_present(self):
        response = AgeCommand.handle(
            {'type': 2,
             'data': {'name': 'slap', 'type': 2,
                      'resolved': {'members': {'1': {'joined_at': (datetime.now() - timedelta(days = 10)).isoformat()}},
                                   'users': {'1': {'username': 'TEST'}}}},
             'token': 'token'})
        assert response['content'] == "<@1> has been a member of this server for 10 days."
