import unittest
from unittest.mock import MagicMock, patch
from uamtbot.utils import Poster
from uamtbot import UamtBot


class TestBotHandler(unittest.TestCase):

    # TODO: proper handle with "mock command handlers" (register overload?)
    # TODO: tests of age handler (yes)

    @patch.object(Poster, 'patch_message')
    def test_handle_message(self, mock_method):
        UamtBot().handle({'type': 2, 'data': {'name': 'slap'}, 'token': 'token'})
        Poster.patch_message.assert_called_with('token', {
            "content": "Sorry, no handler for this command.",
            "allowed_mentions": {
                "parse": []
            }
        })

    @patch.object(Poster, 'post_message')
    def test_handle_interaction(self, mock_method):
        UamtBot().handle({'type': 3, 'token': 'token'})
        Poster.post_message.assert_called_with('token', {
            "content": "Got your interaction. Wink wink.",
            "allowed_mentions": {
                "parse": []
            },
            "flags": (1 << 6)
        })

    def test_ephemeral(self):
        eph = UamtBot().response_ephemeral({'data' : {'name': 'slap', 'options': [{'value': 'test test'}]}})
        assert eph

    def test_ephemeral_age(self):
        eph = UamtBot().response_ephemeral({'data': {'name': 'age', 'type' : 2, 'options': [{'value': 'test test'}]}})
        assert not eph

    def test_get_components(self):
        comp = UamtBot().get_components({'message': {'components': 'RIGHT'}})
        assert comp == 'RIGHT'

    def test_get_command_name(self):
        comp = UamtBot().get_command_name({'data': {'name': 'THis_Is_LiT'}})
        assert comp == 'this_is_lit'

    def test_disable_components(self):
        comp = UamtBot().disable_components([{'type': 2}, {'type': 2}, {'type': 1, 'components': [{'type': 2}, {'type': 2}]}])
        assert comp[0]['disabled']
        assert comp[1]['disabled']
        assert 'disabled' not in comp[2]
        assert comp[2]['components'][0]['disabled']
        assert comp[2]['components'][1]['disabled']

    def test_set_ephemeral(self):
        eph = UamtBot().set_ephemeral({})
        assert eph['flags'] == (1 << 6)
