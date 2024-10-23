
from bibabot.BibaCommand import BibaCommand
import unittest


class TestBibaCommand(unittest.TestCase):

    def test_is_valid_command(self):
        cmd = BibaCommand()
        self.assertTrue(cmd.is_valid_command('/biba'))
        self.assertTrue(cmd.is_valid_command('/biba '))
        self.assertFalse(cmd.is_valid_command('/baba'))
        self.assertFalse(cmd.is_valid_command('biba'))
        self.assertFalse(cmd.is_valid_command('/ biba'))
        self.assertFalse(cmd.is_valid_command('/something_else biba'))
        self.assertFalse(cmd.is_valid_command('something_else /biba'))

    def test_get_message_from_command(self):
        cmd = BibaCommand()
        self.assertEqual(cmd.get_messages_from_command('/biba'), ['Hello this is Bibabot\!'])
        