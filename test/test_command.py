import unittest
from mock import patch, MagicMock
from command import Help, FindTalentsByPerson
from talentbot import SlackEvent
import json

class HelpTest(unittest.TestCase):

    @patch('slackclient.SlackClient')
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

class FindTalentsByPersonTest(unittest.TestCase):

    @patch('slackclient.SlackClient')
    @patch('trello.TrelloClient')
    def setUp(self, slack, trello):
        self.command = FindTalentsByPerson(slack, trello)

    def test_shouldTriggerOnKeywordWithAtSignAndName(self):
        result = self.command.shouldTriggerOn(eventWithText("@ola"))
        self.assertTrue(result)

    def test_shouldTriggerOnSingleAtSign(self):
        result = self.command.shouldTriggerOn(eventWithText("@"))
        self.assertTrue(result)

    def test_shouldNotTriggerOnKeywordWithoutAtSign(self):
        result = self.command.shouldTriggerOn(eventWithText("ola"))
        self.assertFalse(result)

    def test_shouldGiveNoPersonFoundErrorMessageForInvalidUserId(self):
        slackErrMsg = '{"ok":false,"error":"user_not_found"}'
        eventData = SlackEvent(json.loads('{"user":"123","text":"456","channel":789}'))
        self.command.slack.api_call = MagicMock(return_value=slackErrMsg)
        self.command.slack.rtm_send_message = MagicMock(return_value=None)
        self.command.executeOn(eventData)
        self.command.slack.rtm_send_message.assert_called_with(789, 'Ingen person hittades med namnet 56')

    def test_shouldGiveNoTalentsAddedErrorMessageForEmptyTalentList(self):
        slackMsg = '{"ok":true, "user":{"real_name":"testname", "profile":{"email":"test2@citerus.se"}}}'
        eventData = SlackEvent(json.loads('{"user":"123","text":"456","channel":789}'))
        self.command.slack.api_call = MagicMock(return_value=slackMsg)
        self.command.slack.rtm_send_message = MagicMock(return_value=None)
        self.command.trello.getTalentsByEmail = MagicMock(return_value='')
        self.command.executeOn(eventData)
        self.command.slack.rtm_send_message.assert_called_with(789, 'testname har inte lagt till talanger')

def eventWithText(text):
    event = {'text': text}
    return SlackEvent(event)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
