import unittest
from mock import patch, MagicMock
from command import FindPersonsByTalent
from slackevent import SlackEvent, TALENTBOT_USER_ID
import json

exampleUserId = 'U0CJKS2DA'

class FindTalentsByPersonTest(unittest.TestCase):

    @patch('slackclient.SlackClient')
    @patch('trello.TrelloClient')
    def setUp(self, slack, trello):
        self.command = FindPersonsByTalent(slack, trello)

    def test_shouldTriggerOnKeywordWithArgument(self):
        result = self.command.shouldTriggerOn(eventWithText("talent python"))
        self.assertTrue(result)

    def test_shouldSearchForTalentGivenInArgument(self):
        self.command.trello.get_board = MagicMock(return_value='{}')
        self.command.slack.api_call = MagicMock(return_value='{"members":[]}')
        # {"deleted": false, "profile":{"email":"email@gmail.com"}}
        result = self.command.executeOn(eventWithTextAndChannel("talent python", "asdfjkl"))
        #Todo: assert Trello called with "python" 

def eventWithText(text):
    event = {'text': text}
    return SlackEvent(event)

def eventWithTextAndChannel(text, channel):
    event = {'text': text, 'channel': channel}
    return SlackEvent(event)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
