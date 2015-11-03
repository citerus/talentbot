import unittest
from mock import patch, MagicMock
from command import Help, FindTalentsByPerson
from talentbot import SlackEvent, TALENTBOT_USER_ID
import json

exampleUserId = 'U0CJKS2DA'

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

    def test_shouldNotTriggerOnKeywordWithAtSignAndName(self):
        result = self.command.shouldTriggerOn(eventWithText("@ola"))
        self.assertFalse(result)

    def test_shouldNotTriggerOnSingleAtSign(self):
        result = self.command.shouldTriggerOn(eventWithText("@"))
        self.assertFalse(result)

    def test_shouldNotTriggerOnKeywordWithoutAtSign(self):
        result = self.command.shouldTriggerOn(eventWithText("ola"))
        self.assertFalse(result)

    def test_shouldGiveNoPersonFoundErrorMessageForInvalidUserId(self):
        slackErrMsg = '{"ok":false,"error":"user_not_found"}'
        eventData = SlackEvent(json.loads('{"user":"123","text":"456","channel":"D123"}'))
        self.command.slack.api_call = MagicMock(return_value=slackErrMsg)
        self.command.slack.rtm_send_message = MagicMock(return_value=None)

        self.assertTrue(self.command.shouldTriggerOn(eventData))
        self.command.executeOn(eventData)

        self.command.slack.rtm_send_message.assert_called_with("D123", 'Ingen person hittades med namnet 56')

    def test_shouldGiveNoTalentsAddedErrorMessageForEmptyTalentList(self):
        slackMsg = '{"ok":true, "user":{"real_name":"testname", "profile":{"email":"test2@citerus.se", "fields":{}}}}'
        eventData = SlackEvent(json.loads('{"user":"123","text":"456","channel":"D123"}'))
        self.command.slack.api_call = MagicMock(return_value=slackMsg)
        self.command.slack.rtm_send_message = MagicMock(return_value=None)
        self.command.trello.getTalentsByEmail = MagicMock(return_value='')

        self.assertTrue(self.command.shouldTriggerOn(eventData))
        self.command.executeOn(eventData)

        self.command.slack.rtm_send_message.assert_called_with("D123", 'testname har inte lagt till talanger')

    def test_shouldThrowRuntimeErrorForUnknownSlackError(self):
        slackErrMsg = '{"ok":false}'
        eventData = SlackEvent(json.loads('{"user":"123","text":"456","channel":"D123"}'))
        self.command.slack.api_call = MagicMock(return_value=slackErrMsg)
        self.command.slack.rtm_send_message = MagicMock(return_value=None)

        self.command.executeOn(eventData)

        self.command.slack.rtm_send_message.assert_not_called()

    def test_shouldAcceptDirectMessageWithoutAdditionalAddressee(self):
        slackMsg = '{"ok":true, "user":{"real_name":"testname", "profile":{"email":"test2@citerus.se", "fields":{}}}}'
        eventData = SlackEvent(json.loads('{"user":"123","text":"456","channel":"D123"}'))
        self.command.slack.api_call = MagicMock(return_value=slackMsg)
        self.command.slack.rtm_send_message = MagicMock(return_value=None)
        self.command.trello.getTalentsByEmail = MagicMock(return_value='')

        self.assertTrue(self.command.shouldTriggerOn(eventData))
        self.command.executeOn(eventData)

        self.command.slack.rtm_send_message.assert_called_with("D123", 'testname har inte lagt till talanger')

    def test_shouldAcceptIndirectMessageWithAdditionalAddressee(self):
        slackResponse = '{"ok":true, "user":{"real_name":"testname", "profile":{"email":"test2@citerus.se", "fields":{}}}}'
        userIds = '<@{0}>: <@{1}>'.format(TALENTBOT_USER_ID, exampleUserId)
        slackMsg = '{"user":"123","text":"' + userIds + '","channel":"C123"}'
        eventData = SlackEvent(json.loads(slackMsg))
        self.command.slack.api_call = MagicMock(return_value=slackResponse)
        self.command.slack.rtm_send_message = MagicMock(return_value=None)
        self.command.trello.getTalentsByEmail = MagicMock(return_value='')

        self.assertTrue(self.command.shouldTriggerOn(eventData))
        self.command.executeOn(eventData)

        self.command.slack.rtm_send_message.assert_called_with("C123", 'testname har inte lagt till talanger')

    def test_shouldNotAcceptIndirectMessageWithoutAdditionalAddressee(self):
        slackResponse = '{"ok":true, "user":{"real_name":"testname", "profile":{"email":"test2@citerus.se", "fields":{}}}}'
        userIds = '<@{0}>:'.format(TALENTBOT_USER_ID)
        slackMsg = '{"user":"123","text":"' + userIds + '","channel":"C123"}'
        eventData = SlackEvent(json.loads(slackMsg))
        self.command.slack.api_call = MagicMock(return_value=slackResponse)
        self.command.slack.rtm_send_message = MagicMock(return_value=None)
        self.command.trello.getTalentsByEmail = MagicMock(return_value='')

        result = self.command.shouldTriggerOn(eventData)

        self.assertFalse(result)

    def test_shouldAddNoLinksIfNoneAreFound(self):
        slackMsg = '{"ok":true, "user":{"real_name":"testname", "profile":{"email":"test2@citerus.se", "fields":{}}}}'
        eventData = SlackEvent(json.loads('{"user":"123","text":"456","channel":"D123"}'))
        self.command.slack.api_call = MagicMock(return_value=slackMsg)
        self.command.slack.rtm_send_message = MagicMock(return_value=None)
        self.command.trello.getTalentsByEmail = MagicMock(return_value='Java')

        self.assertTrue(self.command.shouldTriggerOn(eventData))
        self.command.executeOn(eventData)

        self.command.slack.rtm_send_message.assert_called_with("D123", 'Om testname: Java')

    def test_shouldAddLinkedInLinkToResponseIfFound(self):
        slackMsg = '{"ok":true, "user":{"real_name":"testname", "profile":{"email":"test2@citerus.se", \
        "fields":{"Xf0DJGDC7M": {"alt": "", "value": "https://www.linkedin.com/profile/view?id=AAAAA"}}}}}'
        eventData = SlackEvent(json.loads('{"user":"123","text":"456","channel":"D123"}'))
        self.command.slack.api_call = MagicMock(return_value=slackMsg)
        self.command.slack.rtm_send_message = MagicMock(return_value=None)
        self.command.trello.getTalentsByEmail = MagicMock(return_value='Java')

        self.assertTrue(self.command.shouldTriggerOn(eventData))
        self.command.executeOn(eventData)

        self.command.slack.rtm_send_message.assert_called_with("D123", 'Om testname: \nLinkedIn: https://www.linkedin.com/profile/view?id=AAAAA \nJava')

    def test_shouldAddMultipleLinksToResponseIfFound(self):
        slackMsg = '{"ok":true, "user":{"real_name":"testname", "profile":{"email":"test2@citerus.se", \
        "fields":{"Xf0DJGDC7M": {"alt": "", "value": "https://www.linkedin.com/profile/view?id=AAAAA"}, \
        "Xf0DJGDC7N": {"alt": "", "value": "https://www.github.com/username/"}}}}}'
        eventData = SlackEvent(json.loads('{"user":"123","text":"456","channel":"D123"}'))
        self.command.slack.api_call = MagicMock(return_value=slackMsg)
        self.command.slack.rtm_send_message = MagicMock(return_value=None)
        self.command.trello.getTalentsByEmail = MagicMock(return_value='Java')

        self.assertTrue(self.command.shouldTriggerOn(eventData))
        self.command.executeOn(eventData)

        self.command.slack.rtm_send_message.assert_called_with("D123", 'Om testname: \nGithub: https://www.github.com/username/ LinkedIn: https://www.linkedin.com/profile/view?id=AAAAA \nJava')

def eventWithText(text):
    event = {'text': text}
    return SlackEvent(event)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
