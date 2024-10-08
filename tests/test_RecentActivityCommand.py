
from bibabot.RecentActivityCommand import RecentActivityCommand
import unittest


class TestRecentActivityCommand(unittest.TestCase):

    def test_is_valid_command(self):
        cmd = RecentActivityCommand(league=None) # No actual League needed
        self.assertTrue(cmd.is_valid_command('/activity'))
        self.assertTrue(cmd.is_valid_command('/activity '))
        self.assertFalse(cmd.is_valid_command(' /activity'))
        self.assertFalse(cmd.is_valid_command('activity'))
        self.assertFalse(cmd.is_valid_command('/ activity'))
        self.assertFalse(cmd.is_valid_command('/something_else activity'))
        self.assertFalse(cmd.is_valid_command('something_else /activity'))

    # TODO: For testing this properly we should have a mock league
    #def test_get_message_from_command(self):
    #    cmd = RecentActivityCommand()
    #    self.assertEqual(cmd.get_messages_from_command('/activity'), ['Hello this is Bibabot!'])
        