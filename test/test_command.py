import unittest
import mock
from command import Help
from talentbot import SlackEvent

class HelpTest(unittest.TestCase):

    @mock.patch('slackclient.SlackClient')
    def setUp(self, slack):
        self.command = Help(slack)

    def test_shouldTriggerOnKeywordWithArgument(self):
        command = self.command
        result = command.shouldTriggerOn(eventWithText("help me"))
        self.assertTrue(result)

    def test_shouldTriggerOnSingleKeyword(self):
        command = self.command
        result = command.shouldTriggerOn(eventWithText("help"))
        self.assertTrue(result)

def eventWithText(text):
    event = {'text': text}
    return SlackEvent(event)

def main():
    unittest.main()

if __name__ == '__main__':
    main()