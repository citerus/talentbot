import unittest
import mock
import json
from command import Help
from talentbot import SlackEvent

class HelpTest(unittest.TestCase):

    @mock.patch('slackclient.SlackClient')
    def setUp(self, slack):
        self.command = Help(slack)

    def test_shouldTriggerOnKeywordWithArgument(self):
        eventJson = json.loads('{"text" : "help me"}')
        event = SlackEvent(eventJson)
        result = self.command.shouldTriggerOn(event)
        self.assertTrue(result)

def main():
    unittest.main()

if __name__ == '__main__':
    main()

