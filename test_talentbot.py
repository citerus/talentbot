import unittest
from talentbot import SlackEvent, TALENTBOT_USER_ID

class SlackEventTest(unittest.TestCase):
    def testCanIdentifyMessage(self):
        event = messageWithText("hej")
        self.assertTrue(event.isMessage())

    def testCanIdentifyMessageFromSelf(self):
        event = messageFromUser(TALENTBOT_USER_ID)
        self.assertTrue(event.isTalentBot())

    def testCanIdentifySingleKeyword(self):
        event = messageWithText("banana")
        self.assertTrue(event.textContainsKeyword("banana"))

    def testCanIdentifyKeywordFollowedByArgument(self):
        event = messageWithText("banana split")
        self.assertTrue(event.textContainsKeyword("banana"))

def messageFromUser(user):
    event = {'type': 'message', 'user': user}
    return SlackEvent(event)

def messageWithText(text):
    event = {'type': 'message', 'text': text}
    return SlackEvent(event)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
