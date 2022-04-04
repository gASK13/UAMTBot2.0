import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from uamtbot.commands.userage import AgeCommand
from uamtbot.commands.age import AgeCommand as ac


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

    @patch.object(ac, 'get_settings')
    def test_age_member_present(self, mock_method):
        response = AgeCommand.handle(
            {'type': 2,
             'data': {'name': 'slap', 'type': 2,
                      'resolved': {'members': {'1': {'joined_at': (datetime.now() - timedelta(days = 10)).isoformat()}},
                                   'users': {'1': {'username': 'TEST'}}}},
             'token': 'token'})
        assert response['content'] == "<@1> has been a member of this server for 10 days."

    @staticmethod
    def fake_settings(id):
        return {'age': {'show': False, 'message': 'Test hide message!'}}


    @patch.object(ac, 'get_settings', fake_settings)
    def test_age_member_present_hidden(self):
        response = AgeCommand.handle(
            {'type': 2,
             'data': {'name': 'slap', 'type': 2,
                      'resolved': {'members': {'1': {'joined_at': (datetime.now() - timedelta(days=10)).isoformat()}},
                                   'users': {'1': {'username': 'TEST'}}}},
             'token': 'token'})
        assert response['content'] == "<@1>'s age is private.\nTest hide message!"
