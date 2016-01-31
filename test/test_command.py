import unittest
from mock import patch, MagicMock
from command import FindPersonsByTalent
from slackevent import TALENTBOT_USER_ID
import json

exampleUserId = 'U0CJKS2DA'
defaultSlackResponse = '{"ok":true, "user":{"real_name":"testname", "profile":{"email":"test2@citerus.se"}}}'

#class FindTalentsByPersonTest(unittest.TestCase):

#    @patch('slackclient.SlackClient')
#    @patch('trello.TrelloClient')
#    def setUp(self, slack, trello):
#        self.command = FindTalentsByPerson(slack, trello)

#    def test_shouldNotTriggerOnKeywordWithAtSignAndName(self):
#        result = self.command.shouldTriggerOn(eventWithText("@ola"))
#        self.assertFalse(result)

#    def test_shouldNotTriggerOnSingleAtSign(self):
#        result = self.command.shouldTriggerOn(eventWithText("@"))
#        self.assertFalse(result)

#    def test_shouldNotTriggerOnKeywordWithoutAtSign(self):
#        result = self.command.shouldTriggerOn(eventWithText("ola"))
#        self.assertFalse(result)

#    def test_shouldGiveNoPersonFoundErrorMessageForInvalidUserId(self):
#        slackErrMsg = '{"ok":false,"error":"user_not_found"}'
#        eventData = SlackEvent(json.loads('{"user":"123","text":"456","channel":"D123"}'))
#        self.command.slack.api_call = MagicMock(return_value=slackErrMsg)

#        self.assertTrue(self.command.shouldTriggerOn(eventData))
#        result = self.command.executeOn(eventData)

#        self.assertEquals(result, 'Ingen person hittades med namnet 56')

#    def test_shouldGiveNoTalentsAddedErrorMessageForEmptyTalentList(self):
#        slackMsg = '{"ok":true, "user":{"real_name":"testname", "profile":{"email":"test2@citerus.se"}}}'
#        eventData = SlackEvent(json.loads('{"user":"123","text":"456","channel":"D123"}'))
#        self.command.slack.api_call = MagicMock(return_value=slackMsg)
#        self.command.trello.getTalentsByEmail = MagicMock(return_value='')

#        self.assertTrue(self.command.shouldTriggerOn(eventData))
#        self.command.executeOn(eventData)

#        self.command.slack.rtm_send_message.assert_called_with("D123", 'testname har inte lagt till talanger')

#    def test_shouldThrowRuntimeErrorForUnknownSlackError(self):
#        slackErrMsg = '{"ok":false}'
#        eventData = SlackEvent(json.loads('{"user":"123","text":"456","channel":"D123"}'))
#        self.command.slack.api_call = MagicMock(return_value=slackErrMsg)
#        self.command.slack.rtm_send_message = MagicMock(return_value=None)

#        self.command.executeOn(eventData)

#        self.command.slack.rtm_send_message.assert_not_called()

#    def test_shouldAcceptDirectMessageWithoutAdditionalAddressee(self):
#        slackMsg = '{"ok":true, "user":{"real_name":"testname", "profile":{"email":"test2@citerus.se"}}}'
#        eventData = SlackEvent(json.loads('{"user":"123","text":"456","channel":"D123"}'))
#        self.command.slack.api_call = MagicMock(return_value=slackMsg)
#        self.command.slack.rtm_send_message = MagicMock(return_value=None)
#        self.command.trello.getTalentsByEmail = MagicMock(return_value='')

#        self.assertTrue(self.command.shouldTriggerOn(eventData))
#        self.command.executeOn(eventData)

#        self.command.slack.rtm_send_message.assert_called_with("D123", 'testname har inte lagt till talanger')

#    def test_shouldAcceptIndirectMessageWithAdditionalAddressee(self):
#        slackResponse = '{"ok":true, "user":{"real_name":"testname", "profile":{"email":"test2@citerus.se"}}}'
#        userIds = '<@{0}>: <@{1}>'.format(TALENTBOT_USER_ID, exampleUserId)
#        slackMsg = '{"user":"123","text":"' + userIds + '","channel":"C123"}'
#        eventData = SlackEvent(json.loads(slackMsg))
#        self.command.slack.api_call = MagicMock(return_value=slackResponse)
#        self.command.slack.rtm_send_message = MagicMock(return_value=None)
#        self.command.trello.getTalentsByEmail = MagicMock(return_value='')

#        self.assertTrue(self.command.shouldTriggerOn(eventData))
#        self.command.executeOn(eventData)

#        self.command.slack.rtm_send_message.assert_called_with("C123", 'testname har inte lagt till talanger')

#    def test_shouldNotAcceptIndirectMessageWithoutAdditionalAddressee(self):
#        slackResponse = '{"ok":true, "user":{"real_name":"testname", "profile":{"email":"test2@citerus.se"}}}'
#        userIds = '<@{0}>:'.format(TALENTBOT_USER_ID)
#        slackMsg = '{"user":"123","text":"' + userIds + '","channel":"C123"}'
#        eventData = SlackEvent(json.loads(slackMsg))
#        self.command.slack.api_call = MagicMock(return_value=slackResponse)
#        self.command.slack.rtm_send_message = MagicMock(return_value=None)
#        self.command.trello.getTalentsByEmail = MagicMock(return_value='')

#        result = self.command.shouldTriggerOn(eventData)

#        self.assertFalse(result)


class FindPersonsByTalentTest(unittest.TestCase):

    @patch('slackclient.SlackClient')
    @patch('trello.TrelloClient')
    def setUp(self, slack, trello):
        self.command = FindPersonsByTalent(slack, trello)

    def test_shouldTriggerOnMessageContainingTalentKeyword(self):
        result = self.command.shouldTriggerOn('java')
        self.assertTrue(result)

    def test_shouldNotTriggerOnMessageMissingKeyword(self):
        result = self.command.shouldTriggerOn('')
        self.assertFalse(result)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
